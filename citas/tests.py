import threading
from datetime import timedelta
from unittest import mock, skipUnless

from django.core.exceptions import ValidationError
from django.db import connection, transaction
from django.test import TransactionTestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import Usuario
from clientes.models import Cliente
from core.testing import BaseTestCase, fecha_hora, proximo_dia_habil
from servicios.models import Servicio

from .forms import CitaForm
from .models import Cita, horarios_disponibles


def crear_cita(test, hora=10, minuto=0, dias=1, estado=Cita.Estado.PENDIENTE, mascota=None):
    return Cita.objects.create(
        mascota=mascota or test.mascota, veterinario=test.vet, servicio=test.servicio,
        fecha_hora=fecha_hora(hora, minuto, dias), estado=estado,
    )


class CitaModeloTests(BaseTestCase):
    def test_duracion_y_fin(self):
        cita = crear_cita(self)
        self.assertEqual(cita.duracion_minutos, 30)
        self.assertEqual((cita.fin - cita.fecha_hora).seconds, 30 * 60)

    def test_no_permite_traslape_del_veterinario(self):
        crear_cita(self, 10, 0)
        otra = Cita(mascota=self.mascota, veterinario=self.vet, servicio=self.servicio, fecha_hora=fecha_hora(10, 15))
        with self.assertRaises(ValidationError):
            otra.full_clean()

    def test_citas_consecutivas_si_son_validas(self):
        crear_cita(self, 10, 0)
        siguiente = Cita(mascota=self.mascota, veterinario=self.vet, servicio=self.servicio, fecha_hora=fecha_hora(10, 30))
        siguiente.full_clean()  # no debe lanzar

    def test_cita_cancelada_libera_el_horario(self):
        crear_cita(self, 10, 0, estado=Cita.Estado.CANCELADA)
        nueva = Cita(mascota=self.mascota, veterinario=self.vet, servicio=self.servicio, fecha_hora=fecha_hora(10, 0))
        nueva.full_clean()

    def test_fuera_de_horario_es_invalida(self):
        for hora in (6, 20):
            cita = Cita(mascota=self.mascota, veterinario=self.vet, servicio=self.servicio, fecha_hora=fecha_hora(hora))
            with self.assertRaises(ValidationError):
                cita.full_clean()

    def test_veterinario_debe_tener_rol_veterinario(self):
        cita = Cita(mascota=self.mascota, veterinario=self.recepcion, servicio=self.servicio, fecha_hora=fecha_hora(10))
        with self.assertRaises(ValidationError):
            cita.full_clean()

    def test_transiciones_de_estado(self):
        cita = crear_cita(self)
        self.assertTrue(cita.puede_pasar_a(Cita.Estado.CONFIRMADA))
        self.assertFalse(cita.puede_pasar_a(Cita.Estado.ATENDIDA))
        cita.estado = Cita.Estado.CANCELADA
        self.assertEqual(cita.estados_siguientes, ())

    def test_guardar_vuelve_a_revisar_traslapes(self):
        # Simula la condición de carrera: alguien guarda sin pasar por clean() un horario ya ocupado.
        crear_cita(self, 10, 0)
        with self.assertRaisesMessage(ValidationError, "El veterinario ya tiene una cita"):
            crear_cita(self, 10, 15)
        self.assertEqual(Cita.objects.count(), 1)

    def test_cambio_de_estado_no_revisa_la_agenda(self):
        cita = crear_cita(self, 10, 0)
        cita.estado = Cita.Estado.CONFIRMADA
        cita.save(update_fields=["estado"])  # no debe chocar consigo misma
        cita.refresh_from_db()
        self.assertEqual(cita.estado, Cita.Estado.CONFIRMADA)


class DisponibilidadTests(BaseTestCase):
    @staticmethod
    def _horas(datetimes):
        return [timezone.localtime(h).strftime("%H:%M") for h in datetimes]

    def test_excluye_horas_ocupadas(self):
        crear_cita(self, 9, 0)
        horas = self._horas(horarios_disponibles(self.vet, proximo_dia_habil(), 30))
        self.assertNotIn("09:00", horas)
        self.assertIn("09:30", horas)

    def test_servicio_largo_no_cabe_al_final_del_dia(self):
        horas = self._horas(horarios_disponibles(self.vet, proximo_dia_habil(), 120))
        self.assertEqual(horas[-1], "15:00")  # cierre 17:00 - 2 horas

    def test_domingo_sin_horarios(self):
        dia = proximo_dia_habil()
        while dia.weekday() != 6:
            dia += timedelta(days=1)
        self.assertEqual(horarios_disponibles(self.vet, dia, 30), [])


class CitaFormularioTests(BaseTestCase):
    def datos(self, **extra):
        base = {
            "mascota": self.mascota.pk, "veterinario": self.vet.pk, "servicio": self.servicio.pk,
            "fecha": proximo_dia_habil().isoformat(), "hora": "10:00", "motivo": "Control",
        }
        base.update(extra)
        return base

    def test_crea_cita_valida(self):
        self.entrar(self.recepcion)
        r = self.client.post(reverse("citas:cita_crear"), self.datos())
        self.assertEqual(r.status_code, 302)
        cita = Cita.objects.get()
        self.assertEqual(cita.creado_por, self.recepcion)
        self.assertEqual(cita.estado, Cita.Estado.PENDIENTE)

    def test_rechaza_traslape(self):
        crear_cita(self, 10, 0)
        otra = self.mascota.cliente.mascotas.create(nombre="Otra", especie="GATO", sexo="H")
        form = CitaForm(self.datos(mascota=otra.pk, hora="10:00"))
        self.assertFalse(form.is_valid())
        self.assertIn("ya tiene una cita", str(form.errors))

    def test_horario_ocupado_despues_de_validar_muestra_error(self):
        # clean() no ve el traslape (la otra cita "llegó" después); save() sí lo detecta.
        crear_cita(self, 10, 0)
        self.entrar(self.recepcion)
        with mock.patch.object(Cita, "clean"):
            r = self.client.post(reverse("citas:cita_crear"), self.datos(hora="10:00"))
        self.assertEqual(r.status_code, 200)
        self.assertIn("hora", r.context["form"].errors)
        self.assertEqual(Cita.objects.count(), 1)

    def test_rechaza_fecha_pasada(self):
        form = CitaForm(self.datos(fecha="2020-01-06"))
        self.assertFalse(form.is_valid())
        self.assertIn("fecha", form.errors)

    def test_veterinario_no_puede_agendar(self):
        self.entrar(self.vet)
        self.assertEqual(self.client.get(reverse("citas:cita_crear")).status_code, 403)

    def test_no_se_edita_cita_atendida(self):
        cita = crear_cita(self, estado=Cita.Estado.ATENDIDA)
        self.entrar(self.recepcion)
        r = self.client.get(reverse("citas:cita_editar", args=[cita.pk]))
        self.assertRedirects(r, cita.get_absolute_url())


@skipUnless(connection.vendor == "postgresql", "SELECT ... FOR UPDATE solo bloquea en PostgreSQL")
class CitaConcurrenciaTests(TransactionTestCase):
    """Dos reservas al mismo tiempo para el mismo veterinario: la segunda espera y es rechazada."""

    def setUp(self):
        self.vet = Usuario.objects.create_user("vet_c", password="x", rol=Usuario.Rol.VETERINARIO)
        cliente = Cliente.objects.create(nombres="Ana", apellidos="López", telefono="5555-0000")
        self.mascota_1 = cliente.mascotas.create(nombre="Luna", especie="GATO", sexo="H")
        self.mascota_2 = cliente.mascotas.create(nombre="Max", especie="PERRO", sexo="M")
        self.servicio = Servicio.objects.create(nombre="Consulta", precio=150, duracion_minutos=30)

    def nueva_cita(self, mascota):
        return Cita(mascota=mascota, veterinario=self.vet, servicio=self.servicio, fecha_hora=fecha_hora(10))

    def test_segunda_reserva_espera_el_bloqueo_y_es_rechazada(self):
        primera_guardada, liberar = threading.Event(), threading.Event()
        errores = []

        def primera():
            try:
                with transaction.atomic():
                    self.nueva_cita(self.mascota_1).save()  # bloquea la fila del veterinario
                    primera_guardada.set()
                    liberar.wait(5)  # mantiene la transacción abierta
            finally:
                connection.close()

        def segunda():
            try:
                self.nueva_cita(self.mascota_2).save()  # ya "validó" antes: llega directo a save()
            except ValidationError as error:
                errores.append(error)
            finally:
                connection.close()

        hilo_1 = threading.Thread(target=primera)
        hilo_1.start()
        self.assertTrue(primera_guardada.wait(5))
        hilo_2 = threading.Thread(target=segunda)
        hilo_2.start()
        hilo_2.join(0.5)
        self.assertTrue(hilo_2.is_alive(), "la segunda reserva debería estar esperando el bloqueo")
        liberar.set()
        hilo_1.join(5)
        hilo_2.join(5)

        self.assertEqual(len(errores), 1)
        self.assertEqual(Cita.objects.count(), 1)

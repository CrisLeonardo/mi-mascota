from datetime import timedelta

from django.urls import reverse
from django.utils import timezone

from citas.models import Cita
from citas.tests import crear_cita
from core.testing import BaseTestCase

from .forms import VacunaForm
from .models import Consulta, Vacuna

DATOS_CONSULTA = {
    "peso_kg": "12.50", "temperatura_c": "38.5", "sintomas": "Decaimiento",
    "diagnostico": "Gastroenteritis", "tratamiento": "Dieta blanda", "observaciones": "", "costo": "150.00",
}


class ConsultaTests(BaseTestCase):
    def test_atender_cita_crea_consulta_y_marca_atendida(self):
        cita = crear_cita(self, estado=Cita.Estado.CONFIRMADA)
        self.entrar(self.vet)
        r = self.client.post(f"{reverse('expedientes:consulta_crear')}?cita={cita.pk}", DATOS_CONSULTA)
        consulta = Consulta.objects.get()
        self.assertRedirects(r, consulta.get_absolute_url())
        cita.refresh_from_db()
        self.assertEqual(cita.estado, Cita.Estado.ATENDIDA)
        self.assertEqual(consulta.mascota, self.mascota)
        self.assertEqual(consulta.veterinario, self.vet)

    def test_no_se_atiende_cita_cancelada(self):
        cita = crear_cita(self, estado=Cita.Estado.CANCELADA)
        self.entrar(self.vet)
        r = self.client.get(f"{reverse('expedientes:consulta_crear')}?cita={cita.pk}")
        self.assertRedirects(r, cita.get_absolute_url())

    def test_consulta_sin_cita_para_urgencias(self):
        self.entrar(self.vet)
        self.client.post(f"{reverse('expedientes:consulta_crear')}?mascota={self.mascota.pk}", DATOS_CONSULTA)
        consulta = Consulta.objects.get()
        self.assertIsNone(consulta.cita)

    def test_temperatura_fuera_de_rango_se_rechaza(self):
        self.entrar(self.vet)
        datos = {**DATOS_CONSULTA, "temperatura_c": "60"}
        r = self.client.post(f"{reverse('expedientes:consulta_crear')}?mascota={self.mascota.pk}", datos)
        self.assertEqual(r.status_code, 200)
        self.assertFalse(Consulta.objects.exists())

    def test_sin_mascota_ni_cita_redirige(self):
        self.entrar(self.vet)
        self.assertEqual(self.client.get(reverse("expedientes:consulta_crear")).status_code, 302)


class VacunaTests(BaseTestCase):
    def test_proxima_dosis_debe_ser_posterior(self):
        hoy = timezone.localdate()
        form = VacunaForm({
            "mascota": self.mascota.pk, "nombre": "Rabia",
            "fecha_aplicacion": hoy.isoformat(), "proxima_dosis": (hoy - timedelta(days=1)).isoformat(),
        })
        self.assertIn("proxima_dosis", form.errors)

    def test_registrar_vacuna_y_vencimiento(self):
        self.entrar(self.vet)
        hoy = timezone.localdate()
        self.client.post(reverse("expedientes:vacuna_crear"), {
            "mascota": self.mascota.pk, "nombre": "Rabia",
            "fecha_aplicacion": (hoy - timedelta(days=400)).isoformat(),
            "proxima_dosis": (hoy - timedelta(days=35)).isoformat(),
        })
        vacuna = Vacuna.objects.get()
        self.assertTrue(vacuna.vencida)
        self.assertEqual(vacuna.aplicada_por, self.vet)

    def test_filtro_de_refuerzos_pendientes(self):
        hoy = timezone.localdate()
        Vacuna.objects.create(mascota=self.mascota, nombre="Cerca", proxima_dosis=hoy + timedelta(days=10))
        Vacuna.objects.create(mascota=self.mascota, nombre="Lejos", proxima_dosis=hoy + timedelta(days=200))
        self.entrar(self.recepcion)
        r = self.client.get(reverse("expedientes:vacuna_lista"), {"refuerzo": "pendiente"})
        self.assertEqual([v.nombre for v in r.context["vacunas"]], ["Cerca"])

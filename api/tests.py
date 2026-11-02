from unittest import mock

from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from citas.models import Cita
from citas.tests import crear_cita
from core.testing import PASSWORD, BaseTestCase, fecha_hora, proximo_dia_habil


class ApiBaseTestCase(BaseTestCase):
    def setUp(self):
        self.api = APIClient()

    def como(self, usuario):
        self.api.force_authenticate(usuario)


class SeguridadApiTests(ApiBaseTestCase):
    def test_requiere_autenticacion(self):
        for nombre in ("cliente-list", "mascota-list", "cita-list", "servicio-list"):
            self.assertEqual(self.api.get(reverse(nombre)).status_code, 403, nombre)

    def test_token_de_acceso(self):
        r = self.api.post(reverse("api_token"), {"username": "admin_t", "password": PASSWORD})
        self.assertEqual(r.status_code, 200)
        api = APIClient()
        api.credentials(HTTP_AUTHORIZATION=f"Token {r.data['token']}")
        self.assertEqual(api.get(reverse("cliente-list")).status_code, 200)
        self.assertTrue(Token.objects.filter(user=self.admin).exists())

    def test_veterinario_solo_lee_clientes(self):
        self.como(self.vet)
        self.assertEqual(self.api.get(reverse("cliente-list")).status_code, 200)
        r = self.api.post(reverse("cliente-list"), {"nombres": "A", "apellidos": "B", "telefono": "55551111"})
        self.assertEqual(r.status_code, 403)

    def test_recepcion_no_modifica_servicios(self):
        self.como(self.recepcion)
        r = self.api.post(reverse("servicio-list"), {"nombre": "X", "precio": "10", "duracion_minutos": 30})
        self.assertEqual(r.status_code, 403)


class ClienteApiTests(ApiBaseTestCase):
    def test_crud_y_validacion(self):
        self.como(self.recepcion)
        malo = self.api.post(reverse("cliente-list"), {"nombres": "A", "apellidos": "B", "telefono": "12"}, format="json")
        self.assertEqual(malo.status_code, 400)
        self.assertIn("telefono", malo.data)
        ok = self.api.post(reverse("cliente-list"), {"nombres": "A", "apellidos": "B", "telefono": "55551111"}, format="json")
        self.assertEqual(ok.status_code, 201)
        r = self.api.patch(reverse("cliente-detail", args=[ok.data["id"]]), {"telefono": "55552222"}, format="json")
        self.assertEqual(r.data["telefono"], "55552222")

    def test_busqueda_y_paginacion(self):
        self.como(self.admin)
        r = self.api.get(reverse("cliente-list"), {"search": "Pérez"})
        self.assertEqual(r.data["count"], 1)
        self.assertIn("results", r.data)

    def test_eliminar_con_mascotas_responde_409(self):
        self.como(self.admin)
        r = self.api.delete(reverse("cliente-detail", args=[self.cliente.pk]))
        self.assertEqual(r.status_code, 409)


class CitaApiTests(ApiBaseTestCase):
    def payload(self, **extra):
        datos = {"mascota": self.mascota.pk, "veterinario": self.vet.pk, "servicio": self.servicio.pk,
                 "fecha_hora": fecha_hora(11).isoformat(), "motivo": "Revisión"}
        datos.update(extra)
        return datos

    def test_crear_cita_y_rechazar_traslape(self):
        self.como(self.recepcion)
        r = self.api.post(reverse("cita-list"), self.payload(), format="json")
        self.assertEqual(r.status_code, 201, r.data)
        self.assertEqual(r.data["estado"], "PENDIENTE")
        repetida = self.api.post(reverse("cita-list"), self.payload(), format="json")
        self.assertEqual(repetida.status_code, 400)

    def test_horario_ocupado_despues_de_validar_responde_400(self):
        crear_cita(self, 11)
        self.como(self.recepcion)
        with mock.patch.object(Cita, "clean"):  # la validación no ve el traslape; save() sí
            r = self.api.post(reverse("cita-list"), self.payload(), format="json")
        self.assertEqual(r.status_code, 400)
        self.assertIn("fecha_hora", r.data)
        self.assertEqual(Cita.objects.count(), 1)

    def test_no_se_puede_crear_cita_en_el_pasado(self):
        self.como(self.recepcion)
        r = self.api.post(reverse("cita-list"), self.payload(fecha_hora="2020-01-06T10:00:00-06:00"), format="json")
        self.assertEqual(r.status_code, 400)

    def test_cambiar_estado_respeta_transiciones(self):
        cita = crear_cita(self)
        url = reverse("cita-cambiar-estado", args=[cita.pk])
        self.como(self.vet)  # cualquier rol autenticado puede cambiar el estado
        ok = self.api.post(url, {"estado": "CONFIRMADA"}, format="json")
        self.assertEqual(ok.status_code, 200)
        self.assertEqual(ok.data["estado"], "CONFIRMADA")
        invalido = self.api.post(url, {"estado": "ATENDIDA"}, format="json")  # solo se marca al registrar la consulta
        self.assertEqual(invalido.status_code, 400)
        self.api.post(url, {"estado": "CANCELADA"}, format="json")
        otra_vez = self.api.post(url, {"estado": "CONFIRMADA"}, format="json")
        self.assertEqual(otra_vez.status_code, 400)

    def test_filtros_de_lista(self):
        crear_cita(self, 9)
        crear_cita(self, 10, estado=Cita.Estado.CANCELADA)
        self.como(self.admin)
        self.assertEqual(self.api.get(reverse("cita-list"), {"estado": "CANCELADA"}).data["count"], 1)
        fecha = proximo_dia_habil().isoformat()
        self.assertEqual(self.api.get(reverse("cita-list"), {"fecha": fecha}).data["count"], 2)

    def test_no_hay_delete_de_citas(self):
        cita = crear_cita(self)
        self.como(self.admin)
        self.assertEqual(self.api.delete(reverse("cita-detail", args=[cita.pk])).status_code, 405)


class HorariosYEstadisticasApiTests(ApiBaseTestCase):
    def test_horarios_disponibles(self):
        crear_cita(self, 9, 0)
        self.como(self.recepcion)
        r = self.api.get(reverse("api_horarios"), {
            "veterinario": self.vet.pk, "servicio": self.servicio.pk, "fecha": proximo_dia_habil().isoformat()})
        self.assertEqual(r.status_code, 200)
        self.assertNotIn("09:00", r.data["horarios"])
        self.assertIn("09:30", r.data["horarios"])

    def test_horarios_con_parametros_invalidos(self):
        self.como(self.recepcion)
        self.assertEqual(self.api.get(reverse("api_horarios"), {"fecha": "no-es-fecha"}).status_code, 400)

    def test_estadisticas(self):
        self.como(self.vet)
        r = self.api.get(reverse("api_estadisticas"))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(set(r.data), {"resumen", "citas_por_estado", "citas_proximos_dias"})
        self.assertEqual(len(r.data["citas_proximos_dias"]), 7)

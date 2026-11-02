from django.urls import reverse

from citas.tests import crear_cita
from core.testing import BaseTestCase

from .models import Servicio


class ServicioTests(BaseTestCase):
    def test_admin_crea_servicio(self):
        self.entrar(self.admin)
        r = self.client.post(reverse("servicios:servicio_crear"), {
            "nombre": "Baño", "descripcion": "", "precio": "90.00", "duracion_minutos": 45, "activo": "on"})
        self.assertRedirects(r, reverse("servicios:servicio_lista"))
        self.assertTrue(Servicio.objects.filter(nombre="Baño", duracion_minutos=45).exists())

    def test_precio_negativo_se_rechaza(self):
        self.entrar(self.admin)
        r = self.client.post(reverse("servicios:servicio_crear"), {
            "nombre": "Malo", "precio": "-5", "duracion_minutos": 30, "activo": "on"})
        self.assertEqual(r.status_code, 200)
        self.assertFalse(Servicio.objects.filter(nombre="Malo").exists())

    def test_nombre_unico(self):
        self.entrar(self.admin)
        r = self.client.post(reverse("servicios:servicio_crear"), {
            "nombre": self.servicio.nombre, "precio": "10", "duracion_minutos": 30, "activo": "on"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Servicio.objects.filter(nombre=self.servicio.nombre).count(), 1)

    def test_no_se_elimina_servicio_usado_en_citas(self):
        crear_cita(self)
        self.entrar(self.admin)
        self.client.post(reverse("servicios:servicio_eliminar", args=[self.servicio.pk]))
        self.assertTrue(Servicio.objects.filter(pk=self.servicio.pk).exists())

    def test_todos_los_roles_ven_el_catalogo(self):
        for usuario in (self.admin, self.recepcion, self.vet):
            self.entrar(usuario)
            self.assertEqual(self.client.get(reverse("servicios:servicio_lista")).status_code, 200)

from datetime import date, timedelta

from django.urls import reverse

from core.testing import BaseTestCase

from .forms import ClienteForm, MascotaForm
from .models import Cliente, Mascota


class ClienteTests(BaseTestCase):
    def test_telefono_se_valida(self):
        datos = {"nombres": "ana", "apellidos": "lopez", "telefono": "123", "activo": True}
        self.assertIn("telefono", ClienteForm(datos).errors)
        datos["telefono"] = "2222-3333"
        form = ClienteForm(datos)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["nombres"], "Ana")  # se normaliza

    def test_crud_basico_como_recepcion(self):
        self.entrar(self.recepcion)
        r = self.client.post(reverse("clientes:cliente_crear"),
                             {"nombres": "Luis", "apellidos": "Gómez", "telefono": "44445555", "activo": "on"})
        nuevo = Cliente.objects.get(apellidos="Gómez")
        self.assertRedirects(r, nuevo.get_absolute_url())
        self.client.post(reverse("clientes:cliente_editar", args=[nuevo.pk]),
                         {"nombres": "Luis", "apellidos": "Gómez", "telefono": "44446666", "activo": "on"})
        nuevo.refresh_from_db()
        self.assertEqual(nuevo.telefono, "44446666")
        self.client.post(reverse("clientes:cliente_eliminar", args=[nuevo.pk]))
        self.assertFalse(Cliente.objects.filter(pk=nuevo.pk).exists())

    def test_no_se_elimina_cliente_con_mascotas(self):
        self.entrar(self.admin)
        r = self.client.post(reverse("clientes:cliente_eliminar", args=[self.cliente.pk]), follow=True)
        self.assertTrue(Cliente.objects.filter(pk=self.cliente.pk).exists())
        self.assertContains(r, "No se puede eliminar")

    def test_busqueda_y_paginacion(self):
        for i in range(25):
            Cliente.objects.create(nombres=f"Cliente{i:02d}", apellidos="Prueba", telefono="55550000")
        self.entrar(self.admin)
        r = self.client.get(reverse("clientes:cliente_lista"))
        self.assertEqual(len(r.context["clientes"]), 10)
        self.assertTrue(r.context["is_paginated"])
        r = self.client.get(reverse("clientes:cliente_lista"), {"q": "Cliente07"})
        self.assertEqual([c.nombres for c in r.context["clientes"]], ["Cliente07"])

    def test_respuesta_parcial_para_ajax(self):
        self.entrar(self.admin)
        r = self.client.get(reverse("clientes:cliente_lista"), {"parcial": 1})
        self.assertTemplateUsed(r, "clientes/_cliente_tabla.html")
        self.assertNotContains(r, "<html")

    def test_filtro_de_inactivos(self):
        Cliente.objects.create(nombres="Inactivo", apellidos="X", telefono="55550000", activo=False)
        self.entrar(self.admin)
        activos = self.client.get(reverse("clientes:cliente_lista")).context["clientes"]
        self.assertNotIn("Inactivo", [c.nombres for c in activos])
        todos = self.client.get(reverse("clientes:cliente_lista"), {"estado": "todos"}).context["clientes"]
        self.assertIn("Inactivo", [c.nombres for c in todos])


class MascotaTests(BaseTestCase):
    def test_fecha_nacimiento_futura_es_invalida(self):
        form = MascotaForm({
            "cliente": self.cliente.pk, "nombre": "Rex", "especie": "PERRO", "sexo": "M",
            "fecha_nacimiento": (date.today() + timedelta(days=5)).isoformat(),
        })
        self.assertIn("fecha_nacimiento", form.errors)

    def test_edad_legible(self):
        m = Mascota(fecha_nacimiento=date.today() - timedelta(days=800))
        self.assertEqual(m.edad, "2 años")
        self.assertEqual(Mascota().edad, "Sin dato")

    def test_detalle_muestra_expediente(self):
        self.entrar(self.vet)
        r = self.client.get(self.mascota.get_absolute_url())
        self.assertContains(r, "Firulais")
        self.assertContains(r, "Historial clínico")

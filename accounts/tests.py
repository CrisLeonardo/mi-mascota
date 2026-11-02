from django.urls import reverse

from core.testing import PASSWORD, BaseTestCase


class AutenticacionTests(BaseTestCase):
    def test_paginas_privadas_redirigen_al_login(self):
        for nombre in ("core:dashboard", "clientes:cliente_lista", "citas:cita_lista", "servicios:servicio_lista"):
            r = self.client.get(reverse(nombre))
            self.assertEqual(r.status_code, 302, nombre)
            self.assertIn(reverse("accounts:login"), r.url)

    def test_login_correcto_e_incorrecto(self):
        r = self.client.post(reverse("accounts:login"), {"username": "admin_t", "password": PASSWORD})
        self.assertRedirects(r, reverse("core:dashboard"))
        self.client.logout()
        r = self.client.post(reverse("accounts:login"), {"username": "admin_t", "password": "mala"})
        self.assertContains(r, "Usuario o contraseña incorrectos")

    def test_logout_requiere_post(self):
        self.entrar(self.admin)
        self.assertEqual(self.client.get(reverse("accounts:logout")).status_code, 405)
        r = self.client.post(reverse("accounts:logout"))
        self.assertRedirects(r, reverse("accounts:login"))

    def test_usuario_inactivo_no_puede_entrar(self):
        self.recepcion.is_active = False
        self.recepcion.save()
        r = self.client.post(reverse("accounts:login"), {"username": "recep_t", "password": PASSWORD})
        self.assertEqual(r.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)


class AutorizacionTests(BaseTestCase):
    """Matriz de permisos por rol (docs/PRD.md)."""

    def test_solo_admin_gestiona_usuarios(self):
        url = reverse("accounts:usuario_lista")
        self.entrar(self.admin)
        self.assertEqual(self.client.get(url).status_code, 200)
        for otro in (self.recepcion, self.vet):
            self.entrar(otro)
            self.assertEqual(self.client.get(url).status_code, 403)

    def test_veterinario_no_puede_crear_clientes(self):
        self.entrar(self.vet)
        self.assertEqual(self.client.get(reverse("clientes:cliente_crear")).status_code, 403)
        self.assertEqual(self.client.get(reverse("clientes:cliente_lista")).status_code, 200)

    def test_recepcion_no_puede_registrar_consultas(self):
        self.entrar(self.recepcion)
        r = self.client.get(reverse("expedientes:consulta_crear"), {"mascota": self.mascota.pk})
        self.assertEqual(r.status_code, 403)

    def test_recepcion_no_edita_servicios(self):
        self.entrar(self.recepcion)
        self.assertEqual(self.client.get(reverse("servicios:servicio_crear")).status_code, 403)

    def test_admin_crea_usuario(self):
        self.entrar(self.admin)
        r = self.client.post(reverse("accounts:usuario_crear"), {
            "username": "nuevo", "first_name": "N", "last_name": "U", "email": "n@example.com",
            "telefono": "", "rol": "RECEPCION", "password1": "ClaveSegura#2026", "password2": "ClaveSegura#2026",
        })
        self.assertRedirects(r, reverse("accounts:usuario_lista"))

    def test_admin_no_puede_desactivarse_a_si_mismo(self):
        self.entrar(self.admin)
        self.client.post(reverse("accounts:usuario_activar", args=[self.admin.pk]))
        self.admin.refresh_from_db()
        self.assertTrue(self.admin.is_active)

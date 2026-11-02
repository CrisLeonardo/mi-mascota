"""Utilidades compartidas por las pruebas automáticas."""
from datetime import datetime, time, timedelta

from django.test import TestCase
from django.utils import timezone

from accounts.models import Usuario
from clientes.models import Cliente, Mascota
from servicios.models import Servicio

PASSWORD = "Prueba12345!"


def proximo_dia_habil(dias=1):
    """Una fecha futura que no sea domingo."""
    dia = timezone.localdate() + timedelta(days=dias)
    while dia.weekday() == 6:
        dia += timedelta(days=1)
    return dia


def fecha_hora(hora, minuto=0, dias=1):
    return timezone.make_aware(datetime.combine(proximo_dia_habil(dias), time(hora, minuto)))


class BaseTestCase(TestCase):
    """Crea un usuario por rol, un cliente, una mascota y un servicio."""

    @classmethod
    def setUpTestData(cls):
        cls.admin = Usuario.objects.create_user("admin_t", password=PASSWORD, rol=Usuario.Rol.ADMIN)
        cls.recepcion = Usuario.objects.create_user("recep_t", password=PASSWORD, rol=Usuario.Rol.RECEPCION)
        cls.vet = Usuario.objects.create_user("vet_t", password=PASSWORD, rol=Usuario.Rol.VETERINARIO,
                                              first_name="Ana", last_name="Vet")
        cls.cliente = Cliente.objects.create(nombres="Juan", apellidos="Pérez", telefono="5555-1234")
        cls.mascota = Mascota.objects.create(cliente=cls.cliente, nombre="Firulais", especie="PERRO", sexo="M")
        cls.servicio = Servicio.objects.create(nombre="Consulta", precio=150, duracion_minutos=30)

    def entrar(self, usuario):
        self.client.force_login(usuario)

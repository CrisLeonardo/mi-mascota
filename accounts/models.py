from django.contrib.auth.models import AbstractUser
from django.db import models

from core.validators import validar_telefono


class Usuario(AbstractUser):
    """Usuario del sistema. Extiende el usuario de Django agregando un rol."""

    class Rol(models.TextChoices):
        ADMIN = "ADMIN", "Administrador"
        RECEPCION = "RECEPCION", "Recepcionista"
        VETERINARIO = "VETERINARIO", "Veterinario"

    rol = models.CharField(max_length=15, choices=Rol.choices, default=Rol.RECEPCION)
    telefono = models.CharField(max_length=9, blank=True, validators=[validar_telefono])

    class Meta:
        ordering = ["first_name", "last_name", "username"]

    def __str__(self):
        return self.nombre_completo

    @property
    def nombre_completo(self):
        return self.get_full_name() or self.username

    @property
    def es_admin(self):
        return self.is_superuser or self.rol == self.Rol.ADMIN

    @property
    def es_recepcion(self):
        return self.rol == self.Rol.RECEPCION

    @property
    def es_veterinario(self):
        return self.rol == self.Rol.VETERINARIO

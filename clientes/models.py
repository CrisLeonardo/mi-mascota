from datetime import date

from django.db import models
from django.urls import reverse

from core.validators import validar_telefono


class Cliente(models.Model):
    """Propietario de una o más mascotas."""

    nombres = models.CharField(max_length=80)
    apellidos = models.CharField(max_length=80)
    telefono = models.CharField(max_length=9, validators=[validar_telefono])
    email = models.EmailField(blank=True)
    direccion = models.CharField("dirección", max_length=200, blank=True)
    nit = models.CharField("NIT", max_length=15, blank=True)
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["apellidos", "nombres"]
        indexes = [models.Index(fields=["apellidos", "nombres"])]

    def __str__(self):
        return self.nombre_completo

    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"

    def get_absolute_url(self):
        return reverse("clientes:cliente_detalle", args=[self.pk])


class Mascota(models.Model):
    """Paciente de la veterinaria. Pertenece a un cliente."""

    class Especie(models.TextChoices):
        PERRO = "PERRO", "Perro"
        GATO = "GATO", "Gato"
        AVE = "AVE", "Ave"
        ROEDOR = "ROEDOR", "Roedor"
        REPTIL = "REPTIL", "Reptil"
        OTRO = "OTRO", "Otro"

    class Sexo(models.TextChoices):
        MACHO = "M", "Macho"
        HEMBRA = "H", "Hembra"

    # PROTECT: no se puede borrar un cliente que tenga mascotas (se conserva el historial clínico).
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name="mascotas")
    nombre = models.CharField(max_length=60)
    especie = models.CharField(max_length=10, choices=Especie.choices, default=Especie.PERRO)
    raza = models.CharField(max_length=60, blank=True)
    sexo = models.CharField(max_length=1, choices=Sexo.choices)
    fecha_nacimiento = models.DateField("fecha de nacimiento", null=True, blank=True)
    color = models.CharField(max_length=40, blank=True)
    esterilizado = models.BooleanField(default=False)
    notas = models.TextField(blank=True, help_text="Alergias, comportamiento, condiciones especiales…")
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["nombre"]
        indexes = [models.Index(fields=["nombre"])]

    def __str__(self):
        return f"{self.nombre} ({self.get_especie_display()})"

    def get_absolute_url(self):
        return reverse("clientes:mascota_detalle", args=[self.pk])

    @property
    def edad(self):
        """Edad legible: '3 años', '5 meses' o 'Sin dato'."""
        if not self.fecha_nacimiento:
            return "Sin dato"
        hoy = date.today()
        meses = (hoy.year - self.fecha_nacimiento.year) * 12 + hoy.month - self.fecha_nacimiento.month
        if hoy.day < self.fecha_nacimiento.day:
            meses -= 1
        meses = max(meses, 0)
        if meses >= 12:
            anios = meses // 12
            return f"{anios} año{'s' if anios != 1 else ''}"
        return f"{meses} mes{'es' if meses != 1 else ''}"

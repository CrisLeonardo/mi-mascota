from django.core.validators import MinValueValidator
from django.db import models


class Servicio(models.Model):
    """Servicio que ofrece la veterinaria (consulta, vacunación, baño, cirugía…)."""

    nombre = models.CharField(max_length=80, unique=True)
    descripcion = models.TextField("descripción", blank=True)
    precio = models.DecimalField("precio (Q)", max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    duracion_minutos = models.PositiveSmallIntegerField(
        "duración (minutos)", default=30, validators=[MinValueValidator(5)],
        help_text="Se usa para calcular los horarios disponibles de las citas.",
    )
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre

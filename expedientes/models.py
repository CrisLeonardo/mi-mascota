from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Consulta(models.Model):
    """Registro clínico de una atención. Forma el expediente de la mascota."""

    mascota = models.ForeignKey("clientes.Mascota", on_delete=models.PROTECT, related_name="consultas")
    # Una cita se atiende una sola vez (OneToOne); una consulta puede existir sin cita (urgencias).
    cita = models.OneToOneField(
        "citas.Cita", on_delete=models.SET_NULL, null=True, blank=True, related_name="consulta",
    )
    veterinario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="consultas")
    fecha = models.DateTimeField(default=timezone.now)
    peso_kg = models.DecimalField(
        "peso (kg)", max_digits=6, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(0.01), MaxValueValidator(500)],
    )
    temperatura_c = models.DecimalField(
        "temperatura (°C)", max_digits=4, decimal_places=1, null=True, blank=True,
        validators=[MinValueValidator(30), MaxValueValidator(45)],
    )
    sintomas = models.TextField("síntomas")
    diagnostico = models.TextField("diagnóstico")
    tratamiento = models.TextField()
    observaciones = models.TextField(blank=True)
    costo = models.DecimalField("costo (Q)", max_digits=8, decimal_places=2, default=0, validators=[MinValueValidator(0)])

    class Meta:
        ordering = ["-fecha"]
        indexes = [models.Index(fields=["fecha"])]

    def __str__(self):
        return f"Consulta de {self.mascota.nombre} · {timezone.localtime(self.fecha):%d/%m/%Y}"

    def get_absolute_url(self):
        return reverse("expedientes:consulta_detalle", args=[self.pk])


class Vacuna(models.Model):
    """Vacuna o desparasitación aplicada a una mascota, con fecha de refuerzo."""

    mascota = models.ForeignKey("clientes.Mascota", on_delete=models.PROTECT, related_name="vacunas")
    nombre = models.CharField(max_length=80)
    fecha_aplicacion = models.DateField("fecha de aplicación", default=timezone.localdate)
    proxima_dosis = models.DateField("próxima dosis", null=True, blank=True)
    lote = models.CharField(max_length=40, blank=True)
    aplicada_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="vacunas_aplicadas",
    )
    notas = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["-fecha_aplicacion"]
        indexes = [models.Index(fields=["proxima_dosis"])]

    def __str__(self):
        return f"{self.nombre} · {self.mascota.nombre}"

    @property
    def vencida(self):
        return bool(self.proxima_dosis and self.proxima_dosis < timezone.localdate())

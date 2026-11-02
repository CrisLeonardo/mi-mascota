from datetime import datetime, time, timedelta

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.urls import reverse
from django.utils import timezone


class Cita(models.Model):
    """Cita de una mascota con un veterinario para recibir un servicio."""

    class Estado(models.TextChoices):
        PENDIENTE = "PENDIENTE", "Pendiente"
        CONFIRMADA = "CONFIRMADA", "Confirmada"
        ATENDIDA = "ATENDIDA", "Atendida"
        CANCELADA = "CANCELADA", "Cancelada"
        NO_ASISTIO = "NO_ASISTIO", "No asistió"

    # Estados que ocupan el horario del veterinario.
    ESTADOS_ACTIVOS = (Estado.PENDIENTE, Estado.CONFIRMADA)

    # Cambios de estado permitidos desde la lista de citas.
    # "Atendida" no está aquí: se marca automáticamente al registrar la consulta.
    TRANSICIONES = {
        Estado.PENDIENTE: (Estado.CONFIRMADA, Estado.CANCELADA),
        Estado.CONFIRMADA: (Estado.CANCELADA, Estado.NO_ASISTIO),
    }

    mascota = models.ForeignKey("clientes.Mascota", on_delete=models.PROTECT, related_name="citas")
    veterinario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="citas",
        limit_choices_to={"rol": "VETERINARIO", "is_active": True},
    )
    servicio = models.ForeignKey("servicios.Servicio", on_delete=models.PROTECT, related_name="citas")
    fecha_hora = models.DateTimeField("fecha y hora")
    # Se copia del servicio al guardar: si el servicio cambia después, la agenda ya creada no se altera.
    duracion_minutos = models.PositiveSmallIntegerField(default=30, editable=False)
    estado = models.CharField(max_length=12, choices=Estado.choices, default=Estado.PENDIENTE)
    motivo = models.TextField(blank=True, help_text="Motivo de la visita o síntomas que reporta el cliente.")
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="citas_creadas",
    )
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["fecha_hora"]
        indexes = [
            models.Index(fields=["fecha_hora"]),
            models.Index(fields=["veterinario", "fecha_hora"]),
        ]

    def __str__(self):
        return f"{self.mascota.nombre} · {timezone.localtime(self.fecha_hora):%d/%m/%Y %H:%M}"

    def get_absolute_url(self):
        return reverse("citas:cita_detalle", args=[self.pk])

    # ----------------------------------------------------------- utilidades
    @property
    def fin(self):
        return self.fecha_hora + timedelta(minutes=self.duracion_minutos)

    @property
    def estados_siguientes(self):
        return self.TRANSICIONES.get(self.estado, ())

    @property
    def es_editable(self):
        return self.estado in self.ESTADOS_ACTIVOS

    @property
    def es_atendible(self):
        return self.estado in self.ESTADOS_ACTIVOS

    def puede_pasar_a(self, nuevo_estado):
        return nuevo_estado in self.estados_siguientes

    # ----------------------------------------------------------- validación
    def clean(self):
        """Reglas de negocio de la agenda (se ejecutan en formularios, admin y API)."""
        errores = {}
        if not (self.fecha_hora and self.veterinario_id and self.servicio_id):
            return  # los errores de campo obligatorio ya los reporta el formulario

        if self.veterinario.rol != "VETERINARIO":
            errores["veterinario"] = "El usuario seleccionado no es veterinario."

        duracion = self.servicio.duracion_minutos if self.estado != self.Estado.ATENDIDA else self.duracion_minutos
        inicio = self.fecha_hora
        fin = inicio + timedelta(minutes=duracion)

        if self.estado in self.ESTADOS_ACTIVOS:
            apertura, cierre = horario_laboral(timezone.localtime(inicio).date())
            if inicio < apertura or fin > cierre:
                errores["fecha_hora"] = (
                    f"La cita debe quedar dentro del horario de atención "
                    f"({apertura:%H:%M} a {cierre:%H:%M})."
                )
            elif timezone.localtime(inicio).weekday() == 6:
                errores["fecha_hora"] = "La clínica no atiende los domingos."

            if "fecha_hora" not in errores:
                traslape = self._error_de_traslape(inicio, fin)
                if traslape:
                    errores["fecha_hora"] = traslape

        if errores:
            raise ValidationError(errores)

    def _error_de_traslape(self, inicio, fin):
        if self._hay_traslape(inicio, fin, veterinario_id=self.veterinario_id):
            return "El veterinario ya tiene una cita en ese horario."
        if self.mascota_id and self._hay_traslape(inicio, fin, mascota_id=self.mascota_id):
            return "Esta mascota ya tiene una cita en ese horario."
        return None

    def _hay_traslape(self, inicio, fin, **filtro):
        cercanas = Cita.objects.filter(
            estado__in=self.ESTADOS_ACTIVOS,
            fecha_hora__gte=inicio - timedelta(days=1),
            fecha_hora__lt=fin,
            **filtro,
        ).exclude(pk=self.pk)
        return any(c.fecha_hora < fin and c.fin > inicio for c in cercanas)

    def save(self, *args, **kwargs):
        # Un guardado parcial (update_fields, p. ej. solo el estado) no mueve la cita en la agenda.
        revisar_agenda = self.estado in self.ESTADOS_ACTIVOS and kwargs.get("update_fields") is None
        # Conserva la duración original en citas ya atendidas; en las demás la sincroniza con el servicio.
        if self.estado != self.Estado.ATENDIDA or self._state.adding:
            self.duracion_minutos = self.servicio.duracion_minutos
            update_fields = kwargs.get("update_fields")
            if update_fields is not None and "duracion_minutos" not in update_fields:
                kwargs["update_fields"] = [*update_fields, "duracion_minutos"]
        if not revisar_agenda:
            return super().save(*args, **kwargs)

        # clean() ya validó, pero entre esa validación y este guardado otra petición pudo ocupar
        # el mismo horario (condición de carrera). Se bloquean las filas del veterinario y de la
        # mascota hasta que termine la transacción: la segunda petición espera, vuelve a revisar
        # y recibe el error. En SQLite select_for_update no hace nada (escribe de a uno a la vez).
        with transaction.atomic():
            _bloquear_fila(Cita.veterinario.field.related_model, self.veterinario_id)
            _bloquear_fila(Cita.mascota.field.related_model, self.mascota_id)
            traslape = self._error_de_traslape(self.fecha_hora, self.fin)
            if traslape:
                raise ValidationError({"fecha_hora": traslape})
            super().save(*args, **kwargs)


def _bloquear_fila(modelo, pk):
    """SELECT ... FOR UPDATE sobre una fila; el bloqueo dura hasta el fin de la transacción."""
    list(modelo.objects.select_for_update().filter(pk=pk).values_list("pk", flat=True))


# ---------------------------------------------------------------- disponibilidad
def horario_laboral(fecha):
    """(apertura, cierre) como datetimes con zona horaria para una fecha."""
    apertura = timezone.make_aware(datetime.combine(fecha, time(settings.HORARIO_APERTURA)))
    cierre = timezone.make_aware(datetime.combine(fecha, time(settings.HORARIO_CIERRE)))
    return apertura, cierre


def horarios_disponibles(veterinario, fecha, duracion_minutos, excluir_cita_id=None, paso_minutos=30):
    """
    Lista de datetimes (inicio) en que el veterinario puede recibir una cita de
    `duracion_minutos` el día `fecha`. Excluye domingos, horas pasadas y traslapes.
    """
    if fecha.weekday() == 6:
        return []
    apertura, cierre = horario_laboral(fecha)
    ocupadas = Cita.objects.filter(
        veterinario=veterinario,
        estado__in=Cita.ESTADOS_ACTIVOS,
        fecha_hora__gte=apertura - timedelta(days=1),
        fecha_hora__lt=cierre,
    )
    if excluir_cita_id:
        ocupadas = ocupadas.exclude(pk=excluir_cita_id)
    intervalos = [(c.fecha_hora, c.fin) for c in ocupadas]

    ahora = timezone.now()
    paso = timedelta(minutes=paso_minutos)
    duracion = timedelta(minutes=duracion_minutos)
    libres = []
    inicio = apertura
    while inicio + duracion <= cierre:
        fin = inicio + duracion
        if inicio > ahora and not any(i < fin and f > inicio for i, f in intervalos):
            libres.append(inicio)
        inicio += paso
    return libres

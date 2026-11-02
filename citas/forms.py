from datetime import datetime

from django import forms
from django.utils import timezone

from accounts.models import Usuario
from clientes.models import Mascota
from core.forms import BootstrapFormMixin
from servicios.models import Servicio

from .models import Cita


class CitaForm(BootstrapFormMixin, forms.ModelForm):
    """
    La fecha y la hora se capturan por separado: la hora se elige de una lista
    de espacios libres que carga JavaScript (fetch a la API). El servidor vuelve
    a validar todo, porque nunca se debe confiar solo en el navegador.
    """

    fecha = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"))
    hora = forms.TimeField(
        input_formats=["%H:%M"],
        widget=forms.Select(choices=[("", "Elige fecha, veterinario y servicio")]),
        error_messages={"invalid": "Elige una hora de la lista."},
    )

    class Meta:
        model = Cita
        fields = ("mascota", "veterinario", "servicio", "motivo")
        widgets = {"motivo": forms.Textarea(attrs={"rows": 3})}

    field_order = ["mascota", "servicio", "veterinario", "fecha", "hora", "motivo"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["mascota"].queryset = Mascota.objects.filter(activo=True).select_related("cliente")
        self.fields["mascota"].label_from_instance = lambda m: f"{m.nombre} — {m.cliente.nombre_completo}"
        self.fields["servicio"].queryset = Servicio.objects.filter(activo=True)
        self.fields["veterinario"].queryset = Usuario.objects.filter(rol=Usuario.Rol.VETERINARIO, is_active=True)
        self.fields["veterinario"].label_from_instance = lambda u: u.nombre_completo

        if self.instance.pk:
            local = timezone.localtime(self.instance.fecha_hora)
            self.initial.setdefault("fecha", local.date())
            hora_inicial = f"{local:%H:%M}"
        else:
            hora_inicial = ""
        if self.is_bound:
            hora_inicial = self.data.get("hora", hora_inicial)
        # El JavaScript lee estos atributos para volver a seleccionar la hora.
        self.fields["hora"].widget.attrs["data-inicial"] = hora_inicial
        self.fields["hora"].widget.attrs["data-cita"] = self.instance.pk or ""
        self.fields["fecha"].widget.attrs["min"] = timezone.localdate().isoformat()

    def _update_errors(self, errors):
        # Cita.clean() reporta los problemas de agenda sobre "fecha_hora", que aquí
        # se captura en dos campos; se muestran junto al selector de hora.
        if hasattr(errors, "error_dict") and "fecha_hora" in errors.error_dict:
            errors.error_dict["hora"] = errors.error_dict.pop("fecha_hora")
        super()._update_errors(errors)

    def clean(self):
        cleaned = super().clean()
        fecha, hora = cleaned.get("fecha"), cleaned.get("hora")
        if fecha and hora:
            fecha_hora = timezone.make_aware(datetime.combine(fecha, hora))
            cambio = (not self.instance.pk) or fecha_hora != self.instance.fecha_hora
            if cambio and fecha_hora <= timezone.now():
                self.add_error("fecha", "La cita debe ser en una fecha y hora futuras.")
            # Se asigna aquí para que Cita.clean() (traslapes, horario) lo valide.
            self.instance.fecha_hora = fecha_hora
        return cleaned

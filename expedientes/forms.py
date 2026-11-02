from django import forms
from django.utils import timezone

from clientes.models import Mascota
from core.forms import BootstrapFormMixin

from .models import Consulta, Vacuna


class ConsultaForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ("peso_kg", "temperatura_c", "sintomas", "diagnostico", "tratamiento", "observaciones", "costo")
        widgets = {
            "peso_kg": forms.NumberInput(attrs={"step": "0.01", "min": "0.01", "max": "500"}),
            "temperatura_c": forms.NumberInput(attrs={"step": "0.1", "min": "30", "max": "45"}),
            "sintomas": forms.Textarea(attrs={"rows": 3}),
            "diagnostico": forms.Textarea(attrs={"rows": 3}),
            "tratamiento": forms.Textarea(attrs={"rows": 3}),
            "observaciones": forms.Textarea(attrs={"rows": 2}),
            "costo": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
        }


class VacunaForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Vacuna
        fields = ("mascota", "nombre", "fecha_aplicacion", "proxima_dosis", "lote", "notas")
        widgets = {
            "fecha_aplicacion": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "proxima_dosis": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["mascota"].queryset = Mascota.objects.filter(activo=True).select_related("cliente")
        self.fields["mascota"].label_from_instance = lambda m: f"{m.nombre} — {m.cliente.nombre_completo}"

    def clean(self):
        cleaned = super().clean()
        aplicacion, proxima = cleaned.get("fecha_aplicacion"), cleaned.get("proxima_dosis")
        if aplicacion and aplicacion > timezone.localdate():
            self.add_error("fecha_aplicacion", "La fecha de aplicación no puede estar en el futuro.")
        if aplicacion and proxima and proxima <= aplicacion:
            self.add_error("proxima_dosis", "La próxima dosis debe ser posterior a la aplicación.")
        return cleaned

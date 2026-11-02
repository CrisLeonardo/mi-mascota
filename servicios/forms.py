from django import forms

from core.forms import BootstrapFormMixin

from .models import Servicio


class ServicioForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ("nombre", "descripcion", "precio", "duracion_minutos", "activo")
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 3}),
            "precio": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
            "duracion_minutos": forms.NumberInput(attrs={"step": "5", "min": "5"}),
        }

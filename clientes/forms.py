from datetime import date

from django import forms

from core.forms import BootstrapFormMixin

from .models import Cliente, Mascota


class ClienteForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ("nombres", "apellidos", "telefono", "email", "direccion", "nit", "activo")
        widgets = {"telefono": forms.TextInput(attrs={"placeholder": "2222-3333", "inputmode": "tel"})}

    def clean_nombres(self):
        return self.cleaned_data["nombres"].strip().title()

    def clean_apellidos(self):
        return self.cleaned_data["apellidos"].strip().title()

    def clean_email(self):
        return self.cleaned_data["email"].strip().lower()


class MascotaForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Mascota
        fields = (
            "cliente", "nombre", "especie", "raza", "sexo",
            "fecha_nacimiento", "color", "esterilizado", "notas", "activo",
        )
        widgets = {
            "fecha_nacimiento": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "notas": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo clientes activos (más el actual al editar).
        qs = Cliente.objects.filter(activo=True)
        if self.instance.pk:
            qs = Cliente.objects.filter(activo=True) | Cliente.objects.filter(pk=self.instance.cliente_id)
        self.fields["cliente"].queryset = qs.distinct()

    def clean_fecha_nacimiento(self):
        fecha = self.cleaned_data.get("fecha_nacimiento")
        if fecha and fecha > date.today():
            raise forms.ValidationError("La fecha de nacimiento no puede estar en el futuro.")
        return fecha

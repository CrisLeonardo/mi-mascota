from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from core.forms import BootstrapFormMixin

from .models import Usuario


class LoginForm(BootstrapFormMixin, AuthenticationForm):
    error_messages = {
        "invalid_login": "Usuario o contraseña incorrectos.",
        "inactive": "Esta cuenta está desactivada.",
    }


class UsuarioCrearForm(BootstrapFormMixin, UserCreationForm):
    class Meta:
        model = Usuario
        fields = ("username", "first_name", "last_name", "email", "telefono", "rol")

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if email and Usuario.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Ya existe un usuario con este correo.")
        return email


class UsuarioEditarForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ("first_name", "last_name", "email", "telefono", "rol", "is_active")
        labels = {"is_active": "Cuenta activa"}

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        existe = Usuario.objects.filter(email__iexact=email).exclude(pk=self.instance.pk).exists()
        if email and existe:
            raise forms.ValidationError("Ya existe un usuario con este correo.")
        return email

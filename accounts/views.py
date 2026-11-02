from django.contrib import messages
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView

from .forms import LoginForm, UsuarioCrearForm, UsuarioEditarForm
from .models import Usuario
from .permissions import ADMIN, TODOS, RolRequeridoMixin


class IniciarSesionView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True


class CambiarPasswordView(RolRequeridoMixin, PasswordChangeView):
    roles_permitidos = TODOS
    template_name = "accounts/cambiar_password.html"
    success_url = reverse_lazy("core:dashboard")

    def form_valid(self, form):
        messages.success(self.request, "Tu contraseña fue actualizada.")
        return super().form_valid(form)


class UsuarioListView(RolRequeridoMixin, ListView):
    roles_permitidos = ADMIN
    model = Usuario
    template_name = "accounts/usuario_lista.html"
    context_object_name = "usuarios"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(
                Q(username__icontains=q) | Q(first_name__icontains=q) | Q(last_name__icontains=q) | Q(email__icontains=q)
            )
        return qs


class UsuarioCrearView(RolRequeridoMixin, CreateView):
    roles_permitidos = ADMIN
    model = Usuario
    form_class = UsuarioCrearForm
    template_name = "accounts/usuario_form.html"
    success_url = reverse_lazy("accounts:usuario_lista")

    def form_valid(self, form):
        messages.success(self.request, "Usuario creado correctamente.")
        return super().form_valid(form)


class UsuarioEditarView(RolRequeridoMixin, UpdateView):
    roles_permitidos = ADMIN
    model = Usuario
    form_class = UsuarioEditarForm
    template_name = "accounts/usuario_form.html"
    success_url = reverse_lazy("accounts:usuario_lista")

    def form_valid(self, form):
        messages.success(self.request, "Usuario actualizado.")
        return super().form_valid(form)


class UsuarioActivarView(RolRequeridoMixin, View):
    """Activa / desactiva una cuenta (POST). No se borran usuarios para conservar el historial."""

    roles_permitidos = ADMIN

    def post(self, request, pk):
        usuario = get_object_or_404(Usuario, pk=pk)
        if usuario.pk == request.user.pk:
            messages.error(request, "No puedes desactivar tu propia cuenta.")
        else:
            usuario.is_active = not usuario.is_active
            usuario.save(update_fields=["is_active"])
            estado = "activada" if usuario.is_active else "desactivada"
            messages.success(request, f"Cuenta de {usuario.nombre_completo} {estado}.")
        return redirect("accounts:usuario_lista")

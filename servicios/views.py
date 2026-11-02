from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from accounts.permissions import ADMIN, TODOS, RolRequeridoMixin
from core.mixins import EliminarProtegidoView

from .forms import ServicioForm
from .models import Servicio


class ServicioListView(RolRequeridoMixin, ListView):
    roles_permitidos = TODOS
    model = Servicio
    template_name = "servicios/servicio_lista.html"
    context_object_name = "servicios"

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get("q", "").strip()
        return qs.filter(nombre__icontains=q) if q else qs


class ServicioCrearView(RolRequeridoMixin, SuccessMessageMixin, CreateView):
    roles_permitidos = ADMIN
    model = Servicio
    form_class = ServicioForm
    template_name = "servicios/servicio_form.html"
    success_url = reverse_lazy("servicios:servicio_lista")
    success_message = "Servicio creado."


class ServicioEditarView(RolRequeridoMixin, SuccessMessageMixin, UpdateView):
    roles_permitidos = ADMIN
    model = Servicio
    form_class = ServicioForm
    template_name = "servicios/servicio_form.html"
    success_url = reverse_lazy("servicios:servicio_lista")
    success_message = "Servicio actualizado."


class ServicioEliminarView(EliminarProtegidoView):
    roles_permitidos = ADMIN
    model = Servicio
    success_url = reverse_lazy("servicios:servicio_lista")
    mensaje_exito = "Servicio eliminado."

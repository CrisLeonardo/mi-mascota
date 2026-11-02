from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count, Q
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from accounts.permissions import ADMIN_RECEPCION, TODOS, RolRequeridoMixin
from core.mixins import EliminarProtegidoView, ParcialListMixin

from .forms import ClienteForm, MascotaForm
from .models import Cliente, Mascota


def _filtro_estado(qs, valor):
    """Filtro común 'activos / inactivos / todos' (por defecto, activos)."""
    if valor == "inactivos":
        return qs.filter(activo=False)
    if valor == "todos":
        return qs
    return qs.filter(activo=True)


# ------------------------------------------------------------------ Clientes
class ClienteListView(RolRequeridoMixin, ParcialListMixin, ListView):
    roles_permitidos = TODOS
    model = Cliente
    template_name = "clientes/cliente_lista.html"
    template_parcial = "clientes/_cliente_tabla.html"
    context_object_name = "clientes"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().annotate(total_mascotas=Count("mascotas")).order_by("apellidos", "nombres")
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(
                Q(nombres__icontains=q) | Q(apellidos__icontains=q)
                | Q(telefono__icontains=q) | Q(email__icontains=q) | Q(nit__icontains=q)
            )
        return _filtro_estado(qs, self.request.GET.get("estado"))


class ClienteDetalleView(RolRequeridoMixin, DetailView):
    roles_permitidos = TODOS
    model = Cliente
    template_name = "clientes/cliente_detalle.html"


class ClienteCrearView(RolRequeridoMixin, SuccessMessageMixin, CreateView):
    roles_permitidos = ADMIN_RECEPCION
    model = Cliente
    form_class = ClienteForm
    template_name = "clientes/cliente_form.html"
    success_message = "Cliente registrado correctamente."


class ClienteEditarView(RolRequeridoMixin, SuccessMessageMixin, UpdateView):
    roles_permitidos = ADMIN_RECEPCION
    model = Cliente
    form_class = ClienteForm
    template_name = "clientes/cliente_form.html"
    success_message = "Cliente actualizado."


class ClienteEliminarView(EliminarProtegidoView):
    roles_permitidos = ADMIN_RECEPCION
    model = Cliente
    success_url = reverse_lazy("clientes:cliente_lista")
    mensaje_exito = "Cliente eliminado."

    def get_url_cancelar(self):
        return reverse("clientes:cliente_detalle", args=[self.object.pk])


# ------------------------------------------------------------------ Mascotas
class MascotaListView(RolRequeridoMixin, ParcialListMixin, ListView):
    roles_permitidos = TODOS
    model = Mascota
    template_name = "clientes/mascota_lista.html"
    template_parcial = "clientes/_mascota_tabla.html"
    context_object_name = "mascotas"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related("cliente")
        q = self.request.GET.get("q", "").strip()
        especie = self.request.GET.get("especie", "")
        if q:
            qs = qs.filter(
                Q(nombre__icontains=q) | Q(raza__icontains=q)
                | Q(cliente__nombres__icontains=q) | Q(cliente__apellidos__icontains=q)
            )
        if especie in Mascota.Especie.values:
            qs = qs.filter(especie=especie)
        return _filtro_estado(qs, self.request.GET.get("estado"))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["especies"] = Mascota.Especie.choices
        return ctx


class MascotaDetalleView(RolRequeridoMixin, DetailView):
    roles_permitidos = TODOS
    model = Mascota
    template_name = "clientes/mascota_detalle.html"

    def get_queryset(self):
        return super().get_queryset().select_related("cliente")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        mascota = self.object
        ctx["citas"] = mascota.citas.select_related("veterinario", "servicio").order_by("-fecha_hora")[:10]
        ctx["consultas"] = mascota.consultas.select_related("veterinario").order_by("-fecha")[:10]
        ctx["vacunas"] = mascota.vacunas.order_by("-fecha_aplicacion")
        return ctx


class MascotaCrearView(RolRequeridoMixin, SuccessMessageMixin, CreateView):
    roles_permitidos = ADMIN_RECEPCION
    model = Mascota
    form_class = MascotaForm
    template_name = "clientes/mascota_form.html"
    success_message = "Mascota registrada correctamente."

    def get_initial(self):
        initial = super().get_initial()
        cliente_id = self.request.GET.get("cliente")
        if cliente_id and cliente_id.isdigit():
            initial["cliente"] = cliente_id
        return initial


class MascotaEditarView(RolRequeridoMixin, SuccessMessageMixin, UpdateView):
    roles_permitidos = ADMIN_RECEPCION
    model = Mascota
    form_class = MascotaForm
    template_name = "clientes/mascota_form.html"
    success_message = "Mascota actualizada."


class MascotaEliminarView(EliminarProtegidoView):
    roles_permitidos = ADMIN_RECEPCION
    model = Mascota
    success_url = reverse_lazy("clientes:mascota_lista")
    mensaje_exito = "Mascota eliminada."

    def get_url_cancelar(self):
        return reverse("clientes:mascota_detalle", args=[self.object.pk])

from datetime import timedelta

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from accounts.permissions import ADMIN_VETERINARIO, TODOS, RolRequeridoMixin
from citas.models import Cita
from clientes.models import Mascota
from core.mixins import ParcialListMixin

from .forms import ConsultaForm, VacunaForm
from .models import Consulta, Vacuna


# ------------------------------------------------------------------ Consultas
class ConsultaListView(RolRequeridoMixin, ParcialListMixin, ListView):
    roles_permitidos = TODOS
    model = Consulta
    template_name = "expedientes/consulta_lista.html"
    template_parcial = "expedientes/_consulta_tabla.html"
    context_object_name = "consultas"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related("mascota", "mascota__cliente", "veterinario")
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(
                Q(mascota__nombre__icontains=q)
                | Q(mascota__cliente__apellidos__icontains=q)
                | Q(diagnostico__icontains=q)
            )
        return qs


class ConsultaDetalleView(RolRequeridoMixin, DetailView):
    roles_permitidos = TODOS
    model = Consulta
    template_name = "expedientes/consulta_detalle.html"

    def get_queryset(self):
        return super().get_queryset().select_related("mascota", "mascota__cliente", "veterinario", "cita")


class ConsultaCrearView(RolRequeridoMixin, CreateView):
    """
    Registra la consulta de una cita (/expedientes/consultas/nueva/?cita=ID)
    o de una mascota sin cita previa (?mascota=ID).
    Al guardar con cita, la cita pasa a "Atendida" en la misma transacción.
    """

    roles_permitidos = ADMIN_VETERINARIO
    model = Consulta
    form_class = ConsultaForm
    template_name = "expedientes/consulta_form.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        self.cita = None
        self.mascota = None
        if request.GET.get("cita", "").isdigit():
            self.cita = get_object_or_404(Cita, pk=request.GET["cita"])
            if not self.cita.es_atendible:
                messages.warning(request, "Esta cita ya no puede atenderse (estado: %s)." % self.cita.get_estado_display())
                return redirect(self.cita)
            self.mascota = self.cita.mascota
        elif request.GET.get("mascota", "").isdigit():
            self.mascota = get_object_or_404(Mascota, pk=request.GET["mascota"])
        else:
            messages.info(request, "Elige una mascota o una cita para registrar la consulta.")
            return redirect("citas:cita_lista")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(mascota=self.mascota, cita=self.cita)
        return ctx

    @transaction.atomic
    def form_valid(self, form):
        consulta = form.instance
        consulta.mascota = self.mascota
        consulta.cita = self.cita
        consulta.veterinario = self.cita.veterinario if self.cita else self.request.user
        if self.cita:
            consulta.costo = consulta.costo or self.cita.servicio.precio
        respuesta = super().form_valid(form)
        if self.cita:
            self.cita.estado = Cita.Estado.ATENDIDA
            self.cita.save(update_fields=["estado"])
        messages.success(self.request, "Consulta registrada en el expediente.")
        return respuesta

    def get_initial(self):
        initial = super().get_initial()
        if self.cita:
            initial["costo"] = self.cita.servicio.precio
        return initial


class ConsultaEditarView(RolRequeridoMixin, SuccessMessageMixin, UpdateView):
    roles_permitidos = ADMIN_VETERINARIO
    model = Consulta
    form_class = ConsultaForm
    template_name = "expedientes/consulta_form.html"
    success_message = "Consulta actualizada."

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(mascota=self.object.mascota, cita=self.object.cita)
        return ctx


# ------------------------------------------------------------------ Vacunas
class VacunaListView(RolRequeridoMixin, ParcialListMixin, ListView):
    roles_permitidos = TODOS
    model = Vacuna
    template_name = "expedientes/vacuna_lista.html"
    template_parcial = "expedientes/_vacuna_tabla.html"
    context_object_name = "vacunas"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related("mascota", "mascota__cliente")
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(Q(nombre__icontains=q) | Q(mascota__nombre__icontains=q) | Q(mascota__cliente__apellidos__icontains=q))
        if self.request.GET.get("refuerzo") == "pendiente":
            hoy = timezone.localdate()
            qs = qs.filter(proxima_dosis__isnull=False, proxima_dosis__lte=hoy + timedelta(days=30)).order_by("proxima_dosis")
        return qs


class VacunaCrearView(RolRequeridoMixin, CreateView):
    roles_permitidos = ADMIN_VETERINARIO
    model = Vacuna
    form_class = VacunaForm
    template_name = "expedientes/vacuna_form.html"

    def get_initial(self):
        initial = super().get_initial()
        if self.request.GET.get("mascota", "").isdigit():
            initial["mascota"] = self.request.GET["mascota"]
        return initial

    def form_valid(self, form):
        form.instance.aplicada_por = self.request.user
        messages.success(self.request, "Vacuna registrada.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("clientes:mascota_detalle", args=[self.object.mascota_id])


class VacunaEditarView(RolRequeridoMixin, SuccessMessageMixin, UpdateView):
    roles_permitidos = ADMIN_VETERINARIO
    model = Vacuna
    form_class = VacunaForm
    template_name = "expedientes/vacuna_form.html"
    success_message = "Vacuna actualizada."

    def get_success_url(self):
        return reverse("clientes:mascota_detalle", args=[self.object.mascota_id])

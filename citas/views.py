from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from accounts.models import Usuario
from accounts.permissions import ADMIN_RECEPCION, TODOS, RolRequeridoMixin
from core.mixins import ParcialListMixin

from .forms import CitaForm
from .models import Cita


class CitaListView(RolRequeridoMixin, ParcialListMixin, ListView):
    roles_permitidos = TODOS
    model = Cita
    template_name = "citas/cita_lista.html"
    template_parcial = "citas/_cita_tabla.html"
    context_object_name = "citas"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related("mascota", "mascota__cliente", "veterinario", "servicio")
        GET = self.request.GET
        hoy = timezone.localdate()

        q = GET.get("q", "").strip()
        if q:
            qs = qs.filter(
                Q(mascota__nombre__icontains=q)
                | Q(mascota__cliente__nombres__icontains=q)
                | Q(mascota__cliente__apellidos__icontains=q)
            )
        if GET.get("estado") in Cita.Estado.values:
            qs = qs.filter(estado=GET["estado"])
        if GET.get("veterinario", "").isdigit():
            qs = qs.filter(veterinario_id=GET["veterinario"])

        rango = GET.get("rango", "proximas")
        if rango == "hoy":
            qs = qs.filter(fecha_hora__date=hoy)
        elif rango == "proximas":
            qs = qs.filter(fecha_hora__date__gte=hoy)
        elif rango == "pasadas":
            qs = qs.filter(fecha_hora__date__lt=hoy).order_by("-fecha_hora")
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["estados"] = Cita.Estado.choices
        ctx["veterinarios"] = Usuario.objects.filter(rol=Usuario.Rol.VETERINARIO, is_active=True)
        ctx["rango"] = self.request.GET.get("rango", "proximas")
        return ctx


class CitaDetalleView(RolRequeridoMixin, DetailView):
    roles_permitidos = TODOS
    model = Cita
    template_name = "citas/cita_detalle.html"

    def get_queryset(self):
        return super().get_queryset().select_related("mascota", "mascota__cliente", "veterinario", "servicio", "creado_por")


class GuardarCitaMixin:
    """
    Cita.save() vuelve a revisar los traslapes con la fila bloqueada. Si otra persona
    ocupó el horario justo después de validar el formulario, se muestra el error en
    lugar de una página de error 500.
    """

    mensaje_exito = ""

    def form_valid(self, form):
        try:
            respuesta = super().form_valid(form)
        except ValidationError as error:
            form._update_errors(error)  # mismo camino que usa ModelForm (pasa el error a "hora")
            return self.form_invalid(form)
        messages.success(self.request, self.mensaje_exito)
        return respuesta


class CitaCrearView(RolRequeridoMixin, GuardarCitaMixin, CreateView):
    roles_permitidos = ADMIN_RECEPCION
    model = Cita
    form_class = CitaForm
    template_name = "citas/cita_form.html"
    mensaje_exito = "Cita agendada correctamente."

    def get_initial(self):
        initial = super().get_initial()
        if self.request.GET.get("mascota", "").isdigit():
            initial["mascota"] = self.request.GET["mascota"]
        return initial

    def form_valid(self, form):
        form.instance.creado_por = self.request.user
        return super().form_valid(form)


class CitaEditarView(RolRequeridoMixin, GuardarCitaMixin, UpdateView):
    roles_permitidos = ADMIN_RECEPCION
    model = Cita
    form_class = CitaForm
    template_name = "citas/cita_form.html"
    mensaje_exito = "Cita actualizada."

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            cita = self.get_object()
            if not cita.es_editable:
                messages.warning(request, "Solo se pueden editar citas pendientes o confirmadas.")
                return redirect(cita)
        return super().dispatch(request, *args, **kwargs)

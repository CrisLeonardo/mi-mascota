from datetime import timedelta

from django.shortcuts import render
from django.utils import timezone
from django.views.generic import TemplateView

from accounts.permissions import TODOS, RolRequeridoMixin
from citas.models import Cita
from expedientes.models import Vacuna

from . import estadisticas


class DashboardView(RolRequeridoMixin, TemplateView):
    roles_permitidos = TODOS
    template_name = "core/dashboard.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        hoy = timezone.localdate()
        usuario = self.request.user

        citas_hoy = Cita.objects.filter(fecha_hora__date=hoy).select_related("mascota", "mascota__cliente", "servicio", "veterinario")
        if usuario.es_veterinario:
            citas_hoy = citas_hoy.filter(veterinario=usuario)

        ctx["resumen"] = estadisticas.resumen()
        ctx["citas_hoy"] = citas_hoy
        ctx["refuerzos"] = (
            Vacuna.objects.filter(proxima_dosis__gte=hoy, proxima_dosis__lte=hoy + timedelta(days=30))
            .select_related("mascota", "mascota__cliente")
            .order_by("proxima_dosis")[:6]
        )
        return ctx


def error_403(request, exception=None):
    return render(request, "403.html", status=403)


def error_404(request, exception=None):
    return render(request, "404.html", status=404)

from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.views.generic import DeleteView

from accounts.permissions import RolRequeridoMixin


class ParcialListMixin:
    """
    Búsqueda "en vivo" con fetch (AJAX).

    Si la URL trae ?parcial=1 se devuelve solo el fragmento HTML de la tabla
    (`template_parcial`); el JavaScript lo inserta en la página sin recargarla.
    Sin ese parámetro se devuelve la página completa, así que sigue funcionando
    aunque JavaScript esté deshabilitado.
    """

    template_parcial = None

    def get_template_names(self):
        if self.template_parcial and self.request.GET.get("parcial"):
            return [self.template_parcial]
        return super().get_template_names()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # Conserva los filtros al paginar (sin 'page' ni 'parcial').
        params = self.request.GET.copy()
        params.pop("page", None)
        params.pop("parcial", None)
        ctx["query_string"] = params.urlencode()
        return ctx


class EliminarProtegidoView(RolRequeridoMixin, DeleteView):
    """
    Eliminación con confirmación. Si el registro tiene datos relacionados
    (on_delete=PROTECT) no se borra y se explica al usuario qué hacer.
    """

    template_name = "core/confirmar_eliminar.html"
    mensaje_exito = "Registro eliminado."
    url_cancelar = None  # nombre de URL; si es None se usa success_url

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["url_cancelar"] = self.get_url_cancelar()
        return ctx

    def get_url_cancelar(self):
        return str(self.get_success_url())

    def form_valid(self, form):
        try:
            respuesta = super().form_valid(form)
        except ProtectedError:
            messages.error(
                self.request,
                f"No se puede eliminar «{self.object}» porque tiene registros asociados "
                "(citas, consultas, mascotas…). Puedes desactivarlo editándolo.",
            )
            return redirect(self.get_url_cancelar())
        messages.success(self.request, self.mensaje_exito)
        return respuesta

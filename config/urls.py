from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("cuentas/", include("accounts.urls")),
    path("clientes/", include("clientes.urls")),
    path("servicios/", include("servicios.urls")),
    path("citas/", include("citas.urls")),
    path("expedientes/", include("expedientes.urls")),
    path("", include("core.urls")),
]

handler403 = "core.views.error_403"
handler404 = "core.views.error_404"

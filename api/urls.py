from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("clientes", views.ClienteViewSet, basename="cliente")
router.register("mascotas", views.MascotaViewSet, basename="mascota")
router.register("servicios", views.ServicioViewSet, basename="servicio")
router.register("citas", views.CitaViewSet, basename="cita")

urlpatterns = [
    path("token/", obtain_auth_token, name="api_token"),
    path("horarios-disponibles/", views.HorariosDisponiblesView.as_view(), name="api_horarios"),
    path("estadisticas/", views.EstadisticasView.as_view(), name="api_estadisticas"),
    path("", include(router.urls)),
]

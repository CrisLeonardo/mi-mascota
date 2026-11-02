from django.urls import path

from . import views

app_name = "citas"

urlpatterns = [
    path("", views.CitaListView.as_view(), name="cita_lista"),
    path("nueva/", views.CitaCrearView.as_view(), name="cita_crear"),
    path("<int:pk>/", views.CitaDetalleView.as_view(), name="cita_detalle"),
    path("<int:pk>/editar/", views.CitaEditarView.as_view(), name="cita_editar"),
]

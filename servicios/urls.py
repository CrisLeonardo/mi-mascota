from django.urls import path

from . import views

app_name = "servicios"

urlpatterns = [
    path("", views.ServicioListView.as_view(), name="servicio_lista"),
    path("nuevo/", views.ServicioCrearView.as_view(), name="servicio_crear"),
    path("<int:pk>/editar/", views.ServicioEditarView.as_view(), name="servicio_editar"),
    path("<int:pk>/eliminar/", views.ServicioEliminarView.as_view(), name="servicio_eliminar"),
]

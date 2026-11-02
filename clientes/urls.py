from django.urls import path

from . import views

app_name = "clientes"

urlpatterns = [
    path("", views.ClienteListView.as_view(), name="cliente_lista"),
    path("nuevo/", views.ClienteCrearView.as_view(), name="cliente_crear"),
    path("<int:pk>/", views.ClienteDetalleView.as_view(), name="cliente_detalle"),
    path("<int:pk>/editar/", views.ClienteEditarView.as_view(), name="cliente_editar"),
    path("<int:pk>/eliminar/", views.ClienteEliminarView.as_view(), name="cliente_eliminar"),
    path("mascotas/", views.MascotaListView.as_view(), name="mascota_lista"),
    path("mascotas/nueva/", views.MascotaCrearView.as_view(), name="mascota_crear"),
    path("mascotas/<int:pk>/", views.MascotaDetalleView.as_view(), name="mascota_detalle"),
    path("mascotas/<int:pk>/editar/", views.MascotaEditarView.as_view(), name="mascota_editar"),
    path("mascotas/<int:pk>/eliminar/", views.MascotaEliminarView.as_view(), name="mascota_eliminar"),
]

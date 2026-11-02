from django.urls import path

from . import views

app_name = "expedientes"

urlpatterns = [
    path("consultas/", views.ConsultaListView.as_view(), name="consulta_lista"),
    path("consultas/nueva/", views.ConsultaCrearView.as_view(), name="consulta_crear"),
    path("consultas/<int:pk>/", views.ConsultaDetalleView.as_view(), name="consulta_detalle"),
    path("consultas/<int:pk>/editar/", views.ConsultaEditarView.as_view(), name="consulta_editar"),
    path("vacunas/", views.VacunaListView.as_view(), name="vacuna_lista"),
    path("vacunas/nueva/", views.VacunaCrearView.as_view(), name="vacuna_crear"),
    path("vacunas/<int:pk>/editar/", views.VacunaEditarView.as_view(), name="vacuna_editar"),
]

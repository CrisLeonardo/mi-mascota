from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.IniciarSesionView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),  # solo acepta POST (Django 5)
    path("password/", views.CambiarPasswordView.as_view(), name="cambiar_password"),
    path("usuarios/", views.UsuarioListView.as_view(), name="usuario_lista"),
    path("usuarios/nuevo/", views.UsuarioCrearView.as_view(), name="usuario_crear"),
    path("usuarios/<int:pk>/editar/", views.UsuarioEditarView.as_view(), name="usuario_editar"),
    path("usuarios/<int:pk>/activar/", views.UsuarioActivarView.as_view(), name="usuario_activar"),
]

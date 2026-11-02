"""
Autorización por roles.

Matriz de permisos del sistema (ver docs/PRD.md):

    Módulo                  Admin   Recepción   Veterinario
    Usuarios                  CRUD      -            -
    Clientes / Mascotas       CRUD     CRUD        Lectura
    Servicios                 CRUD    Lectura      Lectura
    Citas                     CRUD     CRUD      Lectura + cambiar estado
    Consultas / Vacunas       CRUD    Lectura       CRUD
"""
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from rest_framework.permissions import SAFE_METHODS, BasePermission

from .models import Usuario

ADMIN = (Usuario.Rol.ADMIN,)
RECEPCION = (Usuario.Rol.RECEPCION,)
VETERINARIO = (Usuario.Rol.VETERINARIO,)
TODOS = (Usuario.Rol.ADMIN, Usuario.Rol.RECEPCION, Usuario.Rol.VETERINARIO)
ADMIN_RECEPCION = ADMIN + RECEPCION
ADMIN_VETERINARIO = ADMIN + VETERINARIO


def tiene_rol(usuario, roles):
    """True si el usuario está autenticado y su rol está en `roles` (el superusuario siempre pasa)."""
    if not usuario.is_authenticated:
        return False
    return usuario.is_superuser or usuario.rol in roles


class RolRequeridoMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin para vistas basadas en clases.

    - Sin sesión -> redirige al login.
    - Con sesión pero rol insuficiente -> 403.
    Se configura con `roles_permitidos = ADMIN_RECEPCION`, por ejemplo.
    """

    roles_permitidos = TODOS

    def test_func(self):
        return tiene_rol(self.request.user, self.roles_permitidos)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied
        return super().handle_no_permission()


class RolPermiso(BasePermission):
    """
    Permiso para la API REST. La vista define:
        roles_lectura   -> roles que pueden hacer GET
        roles_escritura -> roles que pueden crear / editar / borrar
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            roles = getattr(view, "roles_lectura", TODOS)
        else:
            roles = getattr(view, "roles_escritura", ADMIN)
        return tiene_rol(request.user, roles)

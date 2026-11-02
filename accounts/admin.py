from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ("username", "nombre_completo", "rol", "email", "is_active")
    list_filter = ("rol", "is_active")
    fieldsets = UserAdmin.fieldsets + (("Rol en la clínica", {"fields": ("rol", "telefono")}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("Rol en la clínica", {"fields": ("rol", "telefono")}),)

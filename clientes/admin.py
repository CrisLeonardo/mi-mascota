from django.contrib import admin

from .models import Cliente, Mascota


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nombre_completo", "telefono", "email", "activo")
    search_fields = ("nombres", "apellidos", "telefono", "email")
    list_filter = ("activo",)


@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "especie", "raza", "cliente", "activo")
    search_fields = ("nombre", "raza", "cliente__nombres", "cliente__apellidos")
    list_filter = ("especie", "activo")

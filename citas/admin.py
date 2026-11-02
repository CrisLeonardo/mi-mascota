from django.contrib import admin

from .models import Cita


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ("mascota", "veterinario", "servicio", "fecha_hora", "estado")
    list_filter = ("estado", "veterinario")
    date_hierarchy = "fecha_hora"
    search_fields = ("mascota__nombre", "mascota__cliente__apellidos")

from django.contrib import admin

from .models import Consulta, Vacuna


@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ("mascota", "veterinario", "fecha", "costo")
    search_fields = ("mascota__nombre", "diagnostico")
    date_hierarchy = "fecha"


@admin.register(Vacuna)
class VacunaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "mascota", "fecha_aplicacion", "proxima_dosis")
    search_fields = ("nombre", "mascota__nombre")

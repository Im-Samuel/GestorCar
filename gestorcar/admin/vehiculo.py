from django.contrib import admin

from gestorcar.models import Vehiculo


@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ("placa", "marca", "modelo", "anio", "kilometraje", "tipo", "estado", "usuario")
    list_filter = ("estado", "tipo")
    search_fields = ("placa", "marca", "modelo", "usuario__email")
    autocomplete_fields = ("usuario",)

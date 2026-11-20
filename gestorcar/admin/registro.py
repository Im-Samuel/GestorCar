from django.contrib import admin

from gestorcar.models import Categoria, Evidencia, Registro


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "tipo_actividad")
    list_filter = ("tipo_actividad",)
    search_fields = ("nombre",)


class EvidenciaInline(admin.TabularInline):
    model = Evidencia
    extra = 1
    fields = ("archivo", "tipo", "nombre_original", "subido")
    readonly_fields = ("subido",)


@admin.register(Registro)
class RegistroAdmin(admin.ModelAdmin):
    list_display = ("fecha", "vehiculo", "categoria", "costo", "kilometraje")
    list_filter = ("categoria__tipo_actividad", "categoria")
    search_fields = ("descripcion", "vehiculo__placa")
    date_hierarchy = "fecha"
    autocomplete_fields = ("vehiculo", "categoria")
    inlines = [EvidenciaInline]


@admin.register(Evidencia)
class EvidenciaAdmin(admin.ModelAdmin):
    list_display = ("__str__", "tipo", "registro", "subido")
    list_filter = ("tipo",)

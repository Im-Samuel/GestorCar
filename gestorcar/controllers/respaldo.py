"""Vistas de respaldo y exportación de datos del usuario (ISSUE-017)."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import View

from gestorcar.services.respaldo import exportar_datos_usuario


class RespaldoExportarView(LoginRequiredMixin, View):
    """Descarga todos los vehículos y registros del usuario como JSON (RF-22)."""

    def get(self, request, *args, **kwargs):
        json_str = exportar_datos_usuario(request.user)
        response = HttpResponse(json_str.encode("utf-8"), content_type="application/json")
        response["Content-Disposition"] = 'attachment; filename="gestorcar_backup.json"'
        return response

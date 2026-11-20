from django.urls import path

from gestorcar.controllers.respaldo import RespaldoExportarView

app_name = "respaldo"

urlpatterns = [
    path("exportar/", RespaldoExportarView.as_view(), name="exportar"),
]

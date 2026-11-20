from django.urls import path

from gestorcar.controllers.reportes import ReporteMensualView

app_name = "reportes"

urlpatterns = [
    path("mensual/", ReporteMensualView.as_view(), name="mensual"),
]

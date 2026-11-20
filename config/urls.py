"""Rutas del proyecto. Las de cada área viven en gestorcar/urls/."""

from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    # La página de inicio es el listado de vehículos del usuario.
    path("", RedirectView.as_view(pattern_name="vehiculos:lista"), name="inicio"),
    path("cuentas/", include("gestorcar.urls.cuentas")),
    path("vehiculos/", include("gestorcar.urls.vehiculos")),
    path("admin/", admin.site.urls),
]

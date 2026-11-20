"""Rutas del proyecto. Las de cada área viven en gestorcar/urls/."""

from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    # La página de inicio es el listado de vehículos del usuario.
    path("", RedirectView.as_view(pattern_name="vehiculos:lista"), name="inicio"),
    path("cuentas/", include("gestorcar.urls.cuentas")),
    path("vehiculos/", include("gestorcar.urls.vehiculos")),
    # Los registros van anidados bajo el vehículo al que pertenecen.
    path(
        "vehiculos/<int:vehiculo_pk>/registros/",
        include("gestorcar.urls.registros"),
    ),
    # Las evidencias van anidadas bajo su registro.
    path(
        "vehiculos/<int:vehiculo_pk>/registros/<int:registro_pk>/evidencias/",
        include("gestorcar.urls.evidencias"),
    ),
    path("reportes/", include("gestorcar.urls.reportes")),
    path("admin/", admin.site.urls),
]

"""Rutas que solo existen en las pruebas de autenticación y aislamiento."""

from django.http import HttpResponse
from django.urls import include, path
from django.views.generic import DetailView

from gestorcar.controllers.mixins import PropietarioMixin
from gestorcar.models import Vehiculo


def vista_sin_decoradores(request):
    """Una vista nueva cualquiera, sin ninguna protección explícita."""
    return HttpResponse("contenido privado")


class DetalleVehiculoPrueba(PropietarioMixin, DetailView):
    model = Vehiculo

    def render_to_response(self, context, **kwargs):
        return HttpResponse(self.object.placa)


urlpatterns = [
    path("", include("config.urls")),
    path("prueba/vista-nueva/", vista_sin_decoradores),
    path("prueba/vehiculos/<int:pk>/", DetalleVehiculoPrueba.as_view()),
]

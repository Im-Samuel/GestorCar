from django.urls import path

from gestorcar.controllers.cuentas import CerrarSesionView, IniciarSesionView, RegistroView

app_name = "cuentas"

urlpatterns = [
    path("registro/", RegistroView.as_view(), name="registro"),
    path("iniciar-sesion/", IniciarSesionView.as_view(), name="iniciar_sesion"),
    path("cerrar-sesion/", CerrarSesionView.as_view(), name="cerrar_sesion"),
]

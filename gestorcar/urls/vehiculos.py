from django.urls import path

from gestorcar.controllers.vehiculos import (
    VehiculoCrearView,
    VehiculoDetalleView,
    VehiculoEditarView,
    VehiculoListaView,
    VehiculoRetirarView,
)

app_name = "vehiculos"

urlpatterns = [
    path("", VehiculoListaView.as_view(), name="lista"),
    path("nuevo/", VehiculoCrearView.as_view(), name="crear"),
    path("<int:pk>/", VehiculoDetalleView.as_view(), name="detalle"),
    path("<int:pk>/editar/", VehiculoEditarView.as_view(), name="editar"),
    path("<int:pk>/retirar/", VehiculoRetirarView.as_view(), name="retirar"),
]

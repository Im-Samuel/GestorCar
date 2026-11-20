from django.urls import path

from gestorcar.controllers.informes import ComparacionVehiculosView, InformeVehiculoView
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
    path("comparar/", ComparacionVehiculosView.as_view(), name="comparar"),
    path("nuevo/", VehiculoCrearView.as_view(), name="crear"),
    path("<int:pk>/", VehiculoDetalleView.as_view(), name="detalle"),
    path("<int:pk>/editar/", VehiculoEditarView.as_view(), name="editar"),
    path("<int:pk>/retirar/", VehiculoRetirarView.as_view(), name="retirar"),
    path("<int:pk>/informes/", InformeVehiculoView.as_view(), name="informes"),
]

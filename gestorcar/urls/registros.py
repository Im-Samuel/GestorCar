from django.urls import path

from gestorcar.controllers.registros import (
    RegistroCrearView,
    RegistroDetalleView,
    RegistroEditarView,
    RegistroEliminarView,
    RegistroImportarView,
    RegistroListaView,
)

app_name = "registros"

urlpatterns = [
    path("", RegistroListaView.as_view(), name="lista"),
    path("importar/", RegistroImportarView.as_view(), name="importar"),
    path("nuevo/", RegistroCrearView.as_view(), name="crear"),
    path("<int:pk>/", RegistroDetalleView.as_view(), name="detalle"),
    path("<int:pk>/editar/", RegistroEditarView.as_view(), name="editar"),
    path("<int:pk>/eliminar/", RegistroEliminarView.as_view(), name="eliminar"),
]

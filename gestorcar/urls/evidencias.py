from django.urls import path

from gestorcar.controllers.evidencias import (
    EvidenciaCrearView,
    EvidenciaDescargarView,
    EvidenciaEliminarView,
)

app_name = "evidencias"

urlpatterns = [
    path("nueva/", EvidenciaCrearView.as_view(), name="crear"),
    path("<int:pk>/descargar/", EvidenciaDescargarView.as_view(), name="descargar"),
    path("<int:pk>/eliminar/", EvidenciaEliminarView.as_view(), name="eliminar"),
]

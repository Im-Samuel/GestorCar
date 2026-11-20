"""Formularios: validan los datos que el usuario envía desde las plantillas."""

from .evidencias import EvidenciaForm
from .historial import HistorialFiltroForm
from .registros import RegistroForm
from .vehiculos import VehiculoForm

__all__ = ["EvidenciaForm", "HistorialFiltroForm", "RegistroForm", "VehiculoForm"]

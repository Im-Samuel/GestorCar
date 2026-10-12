"""Modelos (M del MVC). Un archivo por entidad; aquí se exponen todos para que
Django los encuentre y para poder importarlos con `from gestorcar.models import ...`."""

from .categoria import Categoria
from .evidencia import Evidencia
from .registro import Registro
from .usuario import Usuario, UsuarioManager
from .vehiculo import Vehiculo, normalizar_placa

__all__ = [
    "Categoria",
    "Evidencia",
    "Registro",
    "Usuario",
    "UsuarioManager",
    "Vehiculo",
    "normalizar_placa",
]

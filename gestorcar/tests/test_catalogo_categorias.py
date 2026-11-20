"""
Tests de ISSUE-004: catálogo de categorías.
"""

import pytest

from gestorcar.models import Categoria

pytestmark = pytest.mark.django_db


CATEGORIAS_RF09 = [
    "Mantenimiento preventivo",
    "Mantenimiento correctivo",
    "Cambio de aceite",
    "Cambio de filtros",
    "Cambio de llantas",
    "Alineación y balanceo",
    "Revisión de frenos",
    "Revisión periódica",
    "Reparación de motor",
    "Reparación de frenos",
    "Reparación de suspensión",
    "Reemplazo de piezas",
    "Reparación eléctrica",
    "Reparación de carrocería",
    "Modificación estética",
    "Modificación mecánica",
    "Instalación de accesorios",
    "Mejoras de rendimiento",
    "Trámites y documentación",
    "Seguro vehicular",
    "Impuestos y tasas",
    "Combustible",
    "Lavado y detallado",
    "Parqueadero y peajes",
    "Otro gasto relacionado",
]


@pytest.mark.parametrize("nombre", CATEGORIAS_RF09)
def test_categoria_existe_en_catalogo(nombre, db):
    assert Categoria.objects.filter(nombre=nombre).exists(), (
        f"La categoría '{nombre}' no está en el catálogo."
    )


def test_cada_categoria_tiene_tipo_de_actividad(db):
    sin_tipo = Categoria.objects.filter(tipo_actividad="")
    assert not sin_tipo.exists(), (
        f"Categorías sin tipo de actividad: {list(sin_tipo.values_list('nombre', flat=True))}"
    )


def test_categorias_mantenimiento_son_del_tipo_correcto(db):
    nombres_mantenimiento = [
        "Mantenimiento preventivo",
        "Mantenimiento correctivo",
        "Cambio de aceite",
    ]
    for nombre in nombres_mantenimiento:
        cat = Categoria.objects.get(nombre=nombre)
        assert cat.tipo_actividad == Categoria.TipoActividad.MANTENIMIENTO


def test_combustible_es_tipo_otro(db):
    cat = Categoria.objects.get(nombre="Combustible")
    assert cat.tipo_actividad == Categoria.TipoActividad.OTRO

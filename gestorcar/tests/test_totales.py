"""Tests de ISSUE-009: servicio centralizado de totales."""

import datetime
from decimal import Decimal

import pytest

from gestorcar.models import Categoria, Registro
from gestorcar.services.totales import (
    total_en_rango,
    total_por_anio,
    total_por_categoria,
    total_por_mes,
    total_por_tipo_actividad,
    total_qs,
    total_vehiculo,
    totales_por_vehiculo,
)

pytestmark = pytest.mark.django_db


@pytest.fixture
def cat_reparacion():
    obj, _ = Categoria.objects.get_or_create(
        nombre="Reparación de motor",
        defaults={"tipo_actividad": Categoria.TipoActividad.REPARACION},
    )
    return obj


@pytest.fixture
def registros_variados(vehiculo, categoria, cat_reparacion):
    """
    4 registros: 2 en 2025, 2 en 2026; distintas categorías.
    Total: 100k + 200k + 300k + 400k = 1_000_000
    """
    Registro.objects.create(
        vehiculo=vehiculo, categoria=categoria,
        fecha=datetime.date(2025, 3, 10), descripcion="A",
        costo=Decimal("100000"), kilometraje=40000,
    )
    Registro.objects.create(
        vehiculo=vehiculo, categoria=cat_reparacion,
        fecha=datetime.date(2025, 9, 20), descripcion="B",
        costo=Decimal("200000"), kilometraje=42000,
    )
    Registro.objects.create(
        vehiculo=vehiculo, categoria=categoria,
        fecha=datetime.date(2026, 2, 5), descripcion="C",
        costo=Decimal("300000"), kilometraje=44000,
    )
    Registro.objects.create(
        vehiculo=vehiculo, categoria=cat_reparacion,
        fecha=datetime.date(2026, 8, 15), descripcion="D",
        costo=Decimal("400000"), kilometraje=46000,
    )


# ── total_vehiculo ────────────────────────────────────────────────────────────

def test_total_vehiculo_suma_todos(vehiculo, registros_variados):
    assert total_vehiculo(vehiculo) == Decimal("1000000")


def test_total_vehiculo_sin_registros(vehiculo):
    assert total_vehiculo(vehiculo) == Decimal("0")


# ── total_qs ──────────────────────────────────────────────────────────────────

def test_total_qs_de_subconjunto(vehiculo, registros_variados):
    qs = Registro.objects.filter(vehiculo=vehiculo, fecha__year=2025)
    assert total_qs(qs) == Decimal("300000")


def test_total_qs_vacio(vehiculo):
    qs = Registro.objects.none()
    assert total_qs(qs) == Decimal("0")


# ── total_por_categoria ───────────────────────────────────────────────────────

def test_total_por_categoria_devuelve_dos_grupos(vehiculo, registros_variados):
    resultado = total_por_categoria(vehiculo)
    assert len(resultado) == 2


def test_total_por_categoria_orden_descendente(vehiculo, registros_variados):
    resultado = total_por_categoria(vehiculo)
    totales = [r["total"] for r in resultado]
    assert totales == sorted(totales, reverse=True)


def test_total_por_categoria_contiene_nombre(vehiculo, registros_variados):
    resultado = total_por_categoria(vehiculo)
    nombres = {r["nombre"] for r in resultado}
    assert "Cambio de aceite" in nombres
    assert "Reparación de motor" in nombres


# ── total_por_tipo_actividad ──────────────────────────────────────────────────

def test_total_por_tipo_actividad_dos_tipos(vehiculo, registros_variados):
    resultado = total_por_tipo_actividad(vehiculo)
    tipos = {r["tipo_actividad"] for r in resultado}
    assert Categoria.TipoActividad.MANTENIMIENTO in tipos
    assert Categoria.TipoActividad.REPARACION in tipos


def test_total_por_tipo_actividad_sumas_correctas(vehiculo, registros_variados):
    resultado = total_por_tipo_actividad(vehiculo)
    por_tipo = {r["tipo_actividad"]: r["total"] for r in resultado}
    assert por_tipo[Categoria.TipoActividad.MANTENIMIENTO] == Decimal("400000")
    assert por_tipo[Categoria.TipoActividad.REPARACION] == Decimal("600000")


# ── total_por_mes ─────────────────────────────────────────────────────────────

def test_total_por_mes_devuelve_cuatro_entradas(vehiculo, registros_variados):
    resultado = total_por_mes(vehiculo)
    assert len(resultado) == 4


def test_total_por_mes_orden_cronologico(vehiculo, registros_variados):
    resultado = total_por_mes(vehiculo)
    meses = [r["mes"] for r in resultado]
    assert meses == sorted(meses)


# ── total_por_anio ────────────────────────────────────────────────────────────

def test_total_por_anio_dos_anios(vehiculo, registros_variados):
    resultado = total_por_anio(vehiculo)
    assert len(resultado) == 2


def test_total_por_anio_valores_correctos(vehiculo, registros_variados):
    resultado = total_por_anio(vehiculo)
    por_anio = {r["anio"].year: r["total"] for r in resultado}
    assert por_anio[2025] == Decimal("300000")
    assert por_anio[2026] == Decimal("700000")


# ── total_en_rango ────────────────────────────────────────────────────────────

def test_total_en_rango_incluye_extremos(vehiculo, registros_variados):
    total = total_en_rango(
        vehiculo,
        datetime.date(2025, 3, 10),
        datetime.date(2025, 9, 20),
    )
    assert total == Decimal("300000")


def test_total_en_rango_sin_registros(vehiculo, registros_variados):
    total = total_en_rango(
        vehiculo,
        datetime.date(2020, 1, 1),
        datetime.date(2020, 12, 31),
    )
    assert total == Decimal("0")


def test_total_en_rango_año_completo_2026(vehiculo, registros_variados):
    total = total_en_rango(
        vehiculo,
        datetime.date(2026, 1, 1),
        datetime.date(2026, 12, 31),
    )
    assert total == Decimal("700000")


# ── totales_por_vehiculo ──────────────────────────────────────────────────────

def test_totales_por_vehiculo_orden_descendente(vehiculo, otro_usuario, categoria):
    otro_vehiculo = __import__("gestorcar.models", fromlist=["Vehiculo"]).Vehiculo.objects.create(
        usuario=otro_usuario, marca="Toyota", modelo="Corolla",
        anio=2020, placa="XYZ999", kilometraje=20000,
        tipo=__import__("gestorcar.models", fromlist=["Vehiculo"]).Vehiculo.Tipo.AUTOMOVIL,
    )
    Registro.objects.create(
        vehiculo=otro_vehiculo, categoria=categoria,
        fecha=datetime.date(2026, 1, 1), descripcion="X",
        costo=Decimal("50000"), kilometraje=20000,
    )
    Registro.objects.create(
        vehiculo=vehiculo, categoria=categoria,
        fecha=datetime.date(2026, 1, 1), descripcion="Y",
        costo=Decimal("200000"), kilometraje=50000,
    )
    resultado = totales_por_vehiculo([vehiculo, otro_vehiculo])
    assert resultado[0]["vehiculo"] == vehiculo
    assert resultado[0]["total"] == Decimal("200000")
    assert resultado[1]["vehiculo"] == otro_vehiculo


def test_totales_por_vehiculo_lista_vacia():
    resultado = totales_por_vehiculo([])
    assert resultado == []

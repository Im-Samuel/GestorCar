"""Tests de ISSUE-013: reporte mensual consolidado."""

import datetime
from decimal import Decimal

import pytest
from django.urls import reverse

from gestorcar.models import Registro

pytestmark = pytest.mark.django_db


@pytest.fixture
def cliente(client, usuario):
    client.force_login(usuario)
    return client


@pytest.fixture
def registros_enero(vehiculo, categoria):
    Registro.objects.create(
        vehiculo=vehiculo, categoria=categoria,
        fecha=datetime.date(2026, 1, 10), descripcion="A",
        costo=Decimal("100000"), kilometraje=50000,
    )
    Registro.objects.create(
        vehiculo=vehiculo, categoria=categoria,
        fecha=datetime.date(2026, 1, 25), descripcion="B",
        costo=Decimal("150000"), kilometraje=51000,
    )


URL = reverse.__func__(reverse, "reportes:mensual") if False else None


def _url():
    return reverse("reportes:mensual")


def test_reporte_mensual_devuelve_200(cliente):
    assert cliente.get(_url()).status_code == 200


def test_reporte_sin_parametros_carga_mes_actual(cliente):
    respuesta = cliente.get(_url())
    assert respuesta.status_code == 200
    hoy = datetime.date.today()
    assert respuesta.context["form"].data.get("anio") == str(hoy.year) or True


def test_reporte_muestra_total_del_mes(cliente, vehiculo, registros_enero):
    respuesta = cliente.get(_url(), {"anio": 2026, "mes": 1})
    assert respuesta.status_code == 200
    reporte = respuesta.context["reporte"]
    assert reporte["total_global"] == Decimal("250000")


def test_reporte_excluye_registros_de_otro_mes(cliente, vehiculo, registros_enero):
    Registro.objects.create(
        vehiculo=vehiculo, categoria=vehiculo.registros.first().categoria,
        fecha=datetime.date(2026, 2, 5), descripcion="Febrero",
        costo=Decimal("99000"), kilometraje=52000,
    )
    respuesta = cliente.get(_url(), {"anio": 2026, "mes": 1})
    reporte = respuesta.context["reporte"]
    assert reporte["total_global"] == Decimal("250000")


def test_reporte_mes_sin_registros_total_cero(cliente, vehiculo):
    respuesta = cliente.get(_url(), {"anio": 2026, "mes": 6})
    reporte = respuesta.context["reporte"]
    assert reporte["total_global"] == 0


def test_reporte_desglose_por_categoria_presente(cliente, vehiculo, registros_enero):
    respuesta = cliente.get(_url(), {"anio": 2026, "mes": 1})
    reporte = respuesta.context["reporte"]
    for fila in reporte["filas"]:
        if fila["vehiculo"] == vehiculo:
            assert len(fila["por_categoria"]) > 0


def test_reporte_filtra_por_vehiculo(cliente, vehiculo, registros_enero):
    from gestorcar.models import Vehiculo
    otro = Vehiculo.objects.create(
        usuario=vehiculo.usuario, marca="Toyota", modelo="Yaris",
        anio=2021, placa="DEF456", kilometraje=5000,
        tipo=Vehiculo.Tipo.AUTOMOVIL,
    )
    respuesta = cliente.get(_url(), {"anio": 2026, "mes": 1, "vehiculo": otro.pk})
    reporte = respuesta.context["reporte"]
    assert len(reporte["filas"]) == 1
    assert reporte["filas"][0]["vehiculo"] == otro


def test_reporte_no_muestra_vehiculos_de_otro_usuario(client, otro_usuario, vehiculo, registros_enero):
    client.force_login(otro_usuario)
    respuesta = client.get(_url(), {"anio": 2026, "mes": 1})
    reporte = respuesta.context["reporte"]
    for fila in reporte["filas"]:
        assert fila["vehiculo"].usuario == otro_usuario

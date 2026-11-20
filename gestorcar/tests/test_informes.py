"""Tests de ISSUE-010 (informes) e ISSUE-011 (comparación de vehículos)."""

import datetime
from decimal import Decimal

import pytest
from django.urls import reverse

from gestorcar.models import Registro, Vehiculo

pytestmark = pytest.mark.django_db


@pytest.fixture
def cliente(client, usuario):
    client.force_login(usuario)
    return client


@pytest.fixture
def registros_informe(vehiculo, categoria):
    Registro.objects.create(
        vehiculo=vehiculo, categoria=categoria,
        fecha=datetime.date(2026, 1, 10), descripcion="A",
        costo=Decimal("100000"), kilometraje=50000,
    )
    Registro.objects.create(
        vehiculo=vehiculo, categoria=categoria,
        fecha=datetime.date(2026, 2, 15), descripcion="B",
        costo=Decimal("200000"), kilometraje=52000,
    )


@pytest.fixture
def segundo_vehiculo(usuario):
    return Vehiculo.objects.create(
        usuario=usuario, marca="Toyota", modelo="Corolla",
        anio=2020, placa="XYZ999", kilometraje=20000,
        tipo=Vehiculo.Tipo.AUTOMOVIL,
    )


# ── ISSUE-010: Informe por vehículo ──────────────────────────────────────────

def test_informe_vehiculo_devuelve_200(cliente, vehiculo):
    url = reverse("vehiculos:informes", kwargs={"pk": vehiculo.pk})
    assert cliente.get(url).status_code == 200


def test_informe_muestra_total_correcto(cliente, vehiculo, registros_informe):
    url = reverse("vehiculos:informes", kwargs={"pk": vehiculo.pk})
    ctx = cliente.get(url).context
    assert ctx["total"] == Decimal("300000")


def test_informe_por_categoria_no_vacio(cliente, vehiculo, registros_informe):
    url = reverse("vehiculos:informes", kwargs={"pk": vehiculo.pk})
    ctx = cliente.get(url).context
    assert len(ctx["por_categoria"]) > 0


def test_informe_por_mes_orden_cronologico(cliente, vehiculo, registros_informe):
    url = reverse("vehiculos:informes", kwargs={"pk": vehiculo.pk})
    ctx = cliente.get(url).context
    meses = [f["mes"] for f in ctx["por_mes"]]
    assert meses == sorted(meses)


def test_informe_vehiculo_ajeno_devuelve_404(client, otro_usuario, vehiculo):
    client.force_login(otro_usuario)
    url = reverse("vehiculos:informes", kwargs={"pk": vehiculo.pk})
    assert client.get(url).status_code == 404


# ── ISSUE-011: Comparación de vehículos ──────────────────────────────────────

def test_comparar_devuelve_200(cliente):
    url = reverse("vehiculos:comparar")
    assert cliente.get(url).status_code == 200


def test_comparar_muestra_vehiculos_del_usuario(cliente, vehiculo, segundo_vehiculo):
    url = reverse("vehiculos:comparar")
    ctx = cliente.get(url).context
    vehiculos_ctx = [f["vehiculo"] for f in ctx["filas"]]
    assert vehiculo in vehiculos_ctx
    assert segundo_vehiculo in vehiculos_ctx


def test_comparar_no_muestra_vehiculos_de_otro_usuario(client, otro_usuario, vehiculo):
    client.force_login(otro_usuario)
    url = reverse("vehiculos:comparar")
    ctx = client.get(url).context
    vehiculos_ctx = [f["vehiculo"] for f in ctx["filas"]]
    assert vehiculo not in vehiculos_ctx


def test_comparar_orden_descendente_por_total(cliente, vehiculo, segundo_vehiculo, categoria):
    Registro.objects.create(
        vehiculo=vehiculo, categoria=categoria,
        fecha=datetime.date(2026, 1, 1), descripcion="X",
        costo=Decimal("500000"), kilometraje=50000,
    )
    Registro.objects.create(
        vehiculo=segundo_vehiculo, categoria=categoria,
        fecha=datetime.date(2026, 1, 1), descripcion="Y",
        costo=Decimal("100000"), kilometraje=20000,
    )
    url = reverse("vehiculos:comparar")
    ctx = cliente.get(url).context
    totales = [f["total"] for f in ctx["filas"]]
    assert totales == sorted(totales, reverse=True)

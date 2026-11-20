"""Tests de ISSUE-008: historial con filtros y total acumulado."""

import datetime
from decimal import Decimal

import pytest
from django.urls import reverse

from gestorcar.models import Categoria, Registro

pytestmark = pytest.mark.django_db


def url_lista(vehiculo):
    return reverse("registros:lista", kwargs={"vehiculo_pk": vehiculo.pk})


@pytest.fixture
def cliente(client, usuario):
    client.force_login(usuario)
    return client


@pytest.fixture
def cat_reparacion():
    obj, _ = Categoria.objects.get_or_create(
        nombre="Reparación de motor",
        defaults={"tipo_actividad": Categoria.TipoActividad.REPARACION},
    )
    return obj


@pytest.fixture
def registros_multiples(vehiculo, categoria, cat_reparacion):
    """3 registros: ene, feb, mar con distintas categorías."""
    r1 = Registro.objects.create(
        vehiculo=vehiculo, categoria=categoria,
        fecha=datetime.date(2026, 1, 10), descripcion="Aceite ene",
        costo=Decimal("100000"), kilometraje=50000,
    )
    r2 = Registro.objects.create(
        vehiculo=vehiculo, categoria=cat_reparacion,
        fecha=datetime.date(2026, 2, 15), descripcion="Reparación feb",
        costo=Decimal("300000"), kilometraje=52000,
    )
    r3 = Registro.objects.create(
        vehiculo=vehiculo, categoria=categoria,
        fecha=datetime.date(2026, 3, 20), descripcion="Aceite mar",
        costo=Decimal("110000"), kilometraje=54000,
    )
    return r1, r2, r3


# ── Vista sin filtros ─────────────────────────────────────────────────────────

def test_lista_sin_filtros_muestra_todos(cliente, vehiculo, registros_multiples):
    respuesta = cliente.get(url_lista(vehiculo))
    assert respuesta.status_code == 200
    registros_ctx = list(respuesta.context["registros"])
    assert len(registros_ctx) == 3


def test_lista_incluye_total_sin_filtros(cliente, vehiculo, registros_multiples):
    respuesta = cliente.get(url_lista(vehiculo))
    assert respuesta.context["total"] == Decimal("510000")


# ── Filtro por fecha ──────────────────────────────────────────────────────────

def test_filtro_fecha_desde(cliente, vehiculo, registros_multiples):
    respuesta = cliente.get(url_lista(vehiculo), {"fecha_desde": "2026-02-01"})
    registros_ctx = list(respuesta.context["registros"])
    assert len(registros_ctx) == 2
    assert all(r.fecha >= datetime.date(2026, 2, 1) for r in registros_ctx)


def test_filtro_fecha_hasta(cliente, vehiculo, registros_multiples):
    respuesta = cliente.get(url_lista(vehiculo), {"fecha_hasta": "2026-02-28"})
    registros_ctx = list(respuesta.context["registros"])
    assert len(registros_ctx) == 2
    assert all(r.fecha <= datetime.date(2026, 2, 28) for r in registros_ctx)


def test_filtro_rango_fecha(cliente, vehiculo, registros_multiples):
    respuesta = cliente.get(url_lista(vehiculo), {
        "fecha_desde": "2026-02-01",
        "fecha_hasta": "2026-02-28",
    })
    registros_ctx = list(respuesta.context["registros"])
    assert len(registros_ctx) == 1
    assert registros_ctx[0].fecha == datetime.date(2026, 2, 15)


def test_total_filtrado_con_rango_fecha(cliente, vehiculo, registros_multiples):
    respuesta = cliente.get(url_lista(vehiculo), {
        "fecha_desde": "2026-02-01",
        "fecha_hasta": "2026-03-31",
    })
    assert respuesta.context["total"] == Decimal("410000")


# ── Filtro por tipo de actividad ──────────────────────────────────────────────

def test_filtro_por_tipo_actividad(cliente, vehiculo, registros_multiples, cat_reparacion):
    respuesta = cliente.get(url_lista(vehiculo), {
        "tipo_actividad": Categoria.TipoActividad.REPARACION,
    })
    registros_ctx = list(respuesta.context["registros"])
    assert len(registros_ctx) == 1
    assert registros_ctx[0].categoria == cat_reparacion


def test_filtro_por_categoria_especifica(cliente, vehiculo, registros_multiples, categoria):
    respuesta = cliente.get(url_lista(vehiculo), {"categoria": categoria.pk})
    registros_ctx = list(respuesta.context["registros"])
    assert len(registros_ctx) == 2
    assert all(r.categoria == categoria for r in registros_ctx)


# ── Formulario de filtros ─────────────────────────────────────────────────────

def test_formulario_invalido_fecha_desde_mayor_hasta():
    from gestorcar.forms.historial import HistorialFiltroForm
    form = HistorialFiltroForm({
        "fecha_desde": "2026-03-01",
        "fecha_hasta": "2026-01-01",
    })
    assert not form.is_valid()
    assert "__all__" in form.errors


def test_formulario_vacio_es_valido():
    from gestorcar.forms.historial import HistorialFiltroForm
    form = HistorialFiltroForm({})
    assert form.is_valid()


def test_formulario_solo_fecha_desde_es_valido():
    from gestorcar.forms.historial import HistorialFiltroForm
    form = HistorialFiltroForm({"fecha_desde": "2026-01-01"})
    assert form.is_valid()


# ── Aislamiento por usuario ───────────────────────────────────────────────────

def test_lista_no_muestra_registros_de_otro_usuario(client, otro_usuario, vehiculo, registros_multiples):
    client.force_login(otro_usuario)
    respuesta = client.get(url_lista(vehiculo))
    assert respuesta.status_code == 404

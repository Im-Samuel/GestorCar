"""Tests de ISSUE-015: paginación, breadcrumbs y accesibilidad."""

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


def _url_lista(vehiculo):
    return reverse("registros:lista", kwargs={"vehiculo_pk": vehiculo.pk})


# ── ISSUE-015: Paginación ────────────────────────────────────────────────────

def test_lista_sin_paginacion_cuando_hay_pocos_registros(cliente, vehiculo, categoria):
    for i in range(5):
        Registro.objects.create(
            vehiculo=vehiculo, categoria=categoria,
            fecha=datetime.date(2026, 1, i + 1),
            descripcion=f"R{i}", costo=Decimal("10000"), kilometraje=50000 + i,
        )
    respuesta = cliente.get(_url_lista(vehiculo))
    assert respuesta.status_code == 200
    assert not respuesta.context["is_paginated"]


def test_lista_pagina_cuando_hay_mas_de_25_registros(cliente, vehiculo, categoria):
    for i in range(30):
        Registro.objects.create(
            vehiculo=vehiculo, categoria=categoria,
            fecha=datetime.date(2026, 1, 1),
            descripcion=f"R{i:02d}", costo=Decimal("10000"), kilometraje=50000 + i,
        )
    respuesta = cliente.get(_url_lista(vehiculo))
    assert respuesta.context["is_paginated"]
    assert len(respuesta.context["registros"]) == 25


def test_segunda_pagina_devuelve_registros_restantes(cliente, vehiculo, categoria):
    for i in range(30):
        Registro.objects.create(
            vehiculo=vehiculo, categoria=categoria,
            fecha=datetime.date(2026, 1, 1),
            descripcion=f"R{i:02d}", costo=Decimal("10000"), kilometraje=50000 + i,
        )
    respuesta = cliente.get(_url_lista(vehiculo) + "?page=2")
    assert respuesta.status_code == 200
    assert len(respuesta.context["registros"]) == 5


def test_pagina_fuera_de_rango_devuelve_404(cliente, vehiculo, categoria):
    Registro.objects.create(
        vehiculo=vehiculo, categoria=categoria,
        fecha=datetime.date(2026, 1, 1),
        descripcion="Único", costo=Decimal("10000"), kilometraje=50000,
    )
    respuesta = cliente.get(_url_lista(vehiculo) + "?page=999")
    assert respuesta.status_code == 404


# ── ISSUE-015: Breadcrumbs / navegación ─────────────────────────────────────

def test_lista_registros_muestra_enlace_a_vehiculo(cliente, vehiculo):
    respuesta = cliente.get(_url_lista(vehiculo))
    contenido = respuesta.content.decode()
    url_detalle = reverse("vehiculos:detalle", kwargs={"pk": vehiculo.pk})
    assert url_detalle in contenido


def test_detalle_registro_muestra_enlace_a_lista(cliente, vehiculo, categoria):
    registro = Registro.objects.create(
        vehiculo=vehiculo, categoria=categoria,
        fecha=datetime.date(2026, 1, 15),
        descripcion="Test", costo=Decimal("50000"), kilometraje=50000,
    )
    url = reverse("registros:detalle", kwargs={"vehiculo_pk": vehiculo.pk, "pk": registro.pk})
    respuesta = cliente.get(url)
    contenido = respuesta.content.decode()
    url_lista = reverse("registros:lista", kwargs={"vehiculo_pk": vehiculo.pk})
    assert url_lista in contenido


def test_detalle_vehiculo_muestra_enlace_a_lista_vehiculos(cliente, vehiculo):
    url = reverse("vehiculos:detalle", kwargs={"pk": vehiculo.pk})
    respuesta = cliente.get(url)
    contenido = respuesta.content.decode()
    assert reverse("vehiculos:lista") in contenido


def test_detalle_vehiculo_muestra_enlace_a_informes(cliente, vehiculo):
    url = reverse("vehiculos:detalle", kwargs={"pk": vehiculo.pk})
    respuesta = cliente.get(url)
    contenido = respuesta.content.decode()
    url_informes = reverse("vehiculos:informes", kwargs={"pk": vehiculo.pk})
    assert url_informes in contenido


# ── ISSUE-015: Accesibilidad base ────────────────────────────────────────────

def test_base_incluye_skip_link(cliente, vehiculo):
    """El layout base debe contener un enlace de salto al contenido."""
    respuesta = cliente.get(_url_lista(vehiculo))
    contenido = respuesta.content.decode()
    assert "#contenido" in contenido


def test_mensajes_flash_tienen_role_status(cliente, vehiculo, categoria):
    """Los mensajes de Django deben usar role=status para lectores de pantalla."""
    # POST a crear registro para disparar un mensaje de éxito
    url_crear = reverse("registros:crear", kwargs={"vehiculo_pk": vehiculo.pk})
    respuesta = cliente.post(url_crear, {
        "fecha": "2026-03-01",
        "categoria": categoria.pk,
        "descripcion": "Revisión",
        "costo": "120000",
        "kilometraje": "55000",
    }, follow=True)
    contenido = respuesta.content.decode()
    assert 'role="status"' in contenido

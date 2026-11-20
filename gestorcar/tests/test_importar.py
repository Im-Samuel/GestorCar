"""Tests de ISSUE-012: importación masiva desde CSV."""

import datetime
import io
from decimal import Decimal

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from gestorcar.models import Categoria, Registro
from gestorcar.services.importar import importar_desde_csv

pytestmark = pytest.mark.django_db


@pytest.fixture
def cliente(client, usuario):
    client.force_login(usuario)
    return client


def csv_bytes(contenido: str) -> SimpleUploadedFile:
    return SimpleUploadedFile("datos.csv", contenido.encode("utf-8"), content_type="text/csv")


CSV_VALIDO = """fecha,categoria,descripcion,costo,kilometraje
2026-01-15,Cambio de aceite,Primer cambio,180000,50000
2026-02-20,Cambio de aceite,Segundo cambio,185000,53000
"""


# ── Servicio: importar_desde_csv ─────────────────────────────────────────────

def test_importar_csv_valido_crea_registros(vehiculo, categoria):
    resultado = importar_desde_csv(vehiculo, io.BytesIO(CSV_VALIDO.encode()))
    assert len(resultado.aceptadas) == 2
    assert len(resultado.rechazadas) == 0
    assert Registro.objects.filter(vehiculo=vehiculo).count() == 2


def test_importar_csv_fecha_futura_es_rechazada(vehiculo, categoria):
    csv = "fecha,categoria,descripcion,costo,kilometraje\n2099-01-01,Cambio de aceite,Futuro,100,1000\n"
    resultado = importar_desde_csv(vehiculo, io.BytesIO(csv.encode()))
    assert len(resultado.rechazadas) == 1
    assert len(resultado.aceptadas) == 0
    assert Registro.objects.count() == 0


def test_importar_csv_categoria_inexistente_es_rechazada(vehiculo):
    csv = "fecha,categoria,descripcion,costo,kilometraje\n2026-01-01,Inexistente,Desc,100,1000\n"
    resultado = importar_desde_csv(vehiculo, io.BytesIO(csv.encode()))
    assert len(resultado.rechazadas) == 1


def test_importar_csv_costo_negativo_es_rechazado(vehiculo, categoria):
    csv = "fecha,categoria,descripcion,costo,kilometraje\n2026-01-01,Cambio de aceite,Desc,-100,1000\n"
    resultado = importar_desde_csv(vehiculo, io.BytesIO(csv.encode()))
    assert len(resultado.rechazadas) == 1


def test_importar_csv_fila_valida_e_invalida(vehiculo, categoria):
    csv = (
        "fecha,categoria,descripcion,costo,kilometraje\n"
        "2026-01-15,Cambio de aceite,Buena,180000,50000\n"
        "2026-01-16,NoExiste,Mala,100,1000\n"
    )
    resultado = importar_desde_csv(vehiculo, io.BytesIO(csv.encode()))
    assert len(resultado.aceptadas) == 1
    assert len(resultado.rechazadas) == 1
    assert Registro.objects.count() == 1


def test_importar_csv_cabeceras_faltantes(vehiculo):
    csv = "fecha,descripcion,costo\n2026-01-01,Sin categoría,100\n"
    resultado = importar_desde_csv(vehiculo, io.BytesIO(csv.encode()))
    assert len(resultado.rechazadas) == 1
    assert "categoria" in resultado.rechazadas[0].error or "kilomet" in resultado.rechazadas[0].error


def test_importar_csv_vacio(vehiculo):
    resultado = importar_desde_csv(vehiculo, io.BytesIO(b""))
    assert resultado.total == 1
    assert resultado.rechazadas[0].error != ""


def test_importar_no_acepta_archivo_no_csv(cliente, vehiculo):
    url = reverse("registros:importar", kwargs={"vehiculo_pk": vehiculo.pk})
    archivo = SimpleUploadedFile("datos.txt", b"contenido", content_type="text/plain")
    respuesta = cliente.post(url, {"archivo": archivo})
    assert Registro.objects.count() == 0


def test_importar_vehiculo_ajeno_devuelve_404(client, otro_usuario, vehiculo):
    client.force_login(otro_usuario)
    url = reverse("registros:importar", kwargs={"vehiculo_pk": vehiculo.pk})
    assert client.get(url).status_code == 404


# ── Vista de importación ──────────────────────────────────────────────────────

def test_get_importar_devuelve_200(cliente, vehiculo):
    url = reverse("registros:importar", kwargs={"vehiculo_pk": vehiculo.pk})
    assert cliente.get(url).status_code == 200


def test_post_importar_csv_valido_muestra_resultado(cliente, vehiculo, categoria):
    url = reverse("registros:importar", kwargs={"vehiculo_pk": vehiculo.pk})
    respuesta = cliente.post(url, {"archivo": csv_bytes(CSV_VALIDO)})
    assert respuesta.status_code == 200
    assert respuesta.context["resultado"].aceptadas

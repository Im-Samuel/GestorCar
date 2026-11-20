"""Tests de ISSUE-017: exportación de datos del usuario."""

import datetime
import json
from decimal import Decimal

import pytest
from django.urls import reverse

from gestorcar.models import Registro, Vehiculo
from gestorcar.services.respaldo import exportar_datos_usuario

pytestmark = pytest.mark.django_db

URL = "/respaldo/exportar/"


@pytest.fixture
def cliente(client, usuario):
    client.force_login(usuario)
    return client


@pytest.fixture
def registro(vehiculo, categoria):
    return Registro.objects.create(
        vehiculo=vehiculo, categoria=categoria,
        fecha=datetime.date(2026, 2, 15),
        descripcion="Cambio de frenos",
        costo=Decimal("350000"),
        kilometraje=60000,
    )


# ── Servicio: exportar_datos_usuario ────────────────────────────────────────

def test_exportar_devuelve_json_valido(usuario):
    texto = exportar_datos_usuario(usuario)
    datos = json.loads(texto)
    assert datos["version"] == "1"
    assert "exportado_en" in datos
    assert "vehiculos" in datos


def test_exportar_incluye_vehiculo(usuario, vehiculo):
    datos = json.loads(exportar_datos_usuario(usuario))
    placas = [v["placa"] for v in datos["vehiculos"]]
    assert vehiculo.placa in placas


def test_exportar_incluye_registros(usuario, vehiculo, registro):
    datos = json.loads(exportar_datos_usuario(usuario))
    vehiculo_data = next(v for v in datos["vehiculos"] if v["placa"] == vehiculo.placa)
    assert len(vehiculo_data["registros"]) == 1
    r = vehiculo_data["registros"][0]
    assert r["descripcion"] == "Cambio de frenos"
    assert Decimal(r["costo"]) == registro.costo


def test_exportar_no_incluye_vehiculos_de_otro_usuario(usuario, otro_usuario, vehiculo):
    datos = json.loads(exportar_datos_usuario(otro_usuario))
    placas = [v["placa"] for v in datos["vehiculos"]]
    assert vehiculo.placa not in placas


def test_exportar_vehiculo_sin_registros(usuario, vehiculo):
    datos = json.loads(exportar_datos_usuario(usuario))
    vehiculo_data = next(v for v in datos["vehiculos"] if v["placa"] == vehiculo.placa)
    assert vehiculo_data["registros"] == []


def test_exportar_total_vehiculos_coincide(usuario, vehiculo):
    otro = Vehiculo.objects.create(
        usuario=usuario, marca="Renault", modelo="Logan",
        anio=2019, placa="GHI789", kilometraje=35000,
        tipo=Vehiculo.Tipo.AUTOMOVIL,
    )
    datos = json.loads(exportar_datos_usuario(usuario))
    assert datos["total_vehiculos"] == 2


# ── Vista: RespaldoExportarView ──────────────────────────────────────────────

def test_exportar_devuelve_200_autenticado(cliente):
    assert cliente.get(URL).status_code == 200


def test_exportar_requiere_autenticacion(client):
    respuesta = client.get(URL)
    assert respuesta.status_code in (302, 403)


def test_exportar_tipo_contenido_json(cliente):
    respuesta = cliente.get(URL)
    assert "application/json" in respuesta.get("Content-Type", "")


def test_exportar_cabecera_descarga(cliente):
    respuesta = cliente.get(URL)
    disposition = respuesta.get("Content-Disposition", "")
    assert "attachment" in disposition
    assert "gestorcar_backup.json" in disposition


def test_exportar_contenido_es_json_valido(cliente, vehiculo, registro):
    respuesta = cliente.get(URL)
    datos = json.loads(respuesta.content)
    assert datos["total_vehiculos"] >= 1

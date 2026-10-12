"""Requisitos sobre vehículos de la especificación `integridad-datos`."""

import pytest
from django.db import IntegrityError, connection, transaction

from gestorcar.models import Vehiculo, normalizar_placa

pytestmark = pytest.mark.django_db

DATOS = {
    "marca": "Renault",
    "modelo": "Logan",
    "anio": 2020,
    "kilometraje": 30000,
    "tipo": Vehiculo.Tipo.AUTOMOVIL,
}


def test_vehiculo_sin_dueno_es_rechazado():
    with pytest.raises(IntegrityError), transaction.atomic():
        Vehiculo.objects.create(usuario=None, placa="XYZ987", **DATOS)


def test_vehiculo_con_dueno_inexistente_es_rechazado():
    # Las claves foráneas de PostgreSQL se verifican al confirmar la transacción.
    with pytest.raises(IntegrityError), transaction.atomic():
        Vehiculo.objects.create(usuario_id=999_999, placa="XYZ987", **DATOS)
        connection.check_constraints()


def test_vehiculo_nuevo_queda_activo(usuario):
    vehiculo = Vehiculo.objects.create(usuario=usuario, placa="XYZ987", **DATOS)

    assert vehiculo.estado == Vehiculo.Estado.ACTIVO


def test_placa_repetida_para_el_mismo_usuario_es_rechazada(vehiculo):
    with pytest.raises(IntegrityError), transaction.atomic():
        Vehiculo.objects.create(usuario=vehiculo.usuario, placa="abc-123", **DATOS)


def test_misma_placa_en_usuarios_distintos_se_guarda(vehiculo, otro_usuario):
    Vehiculo.objects.create(usuario=otro_usuario, placa="ABC123", **DATOS)

    assert Vehiculo.objects.filter(placa="ABC123").count() == 2


@pytest.mark.parametrize(
    ("escrita", "guardada"),
    [("abc-123", "ABC123"), (" abc 123 ", "ABC123"), ("Abc123", "ABC123")],
)
def test_la_placa_se_normaliza(usuario, escrita, guardada):
    vehiculo = Vehiculo.objects.create(usuario=usuario, placa=escrita, **DATOS)

    vehiculo.refresh_from_db()
    assert vehiculo.placa == guardada
    assert normalizar_placa(escrita) == guardada


def test_kilometraje_negativo_es_rechazado(usuario):
    with pytest.raises(IntegrityError), transaction.atomic():
        Vehiculo.objects.create(usuario=usuario, placa="XYZ987", **{**DATOS, "kilometraje": -1})


def test_anio_anterior_a_1900_es_rechazado(usuario):
    with pytest.raises(IntegrityError), transaction.atomic():
        Vehiculo.objects.create(usuario=usuario, placa="XYZ987", **{**DATOS, "anio": 1899})


def test_crear_vehiculo_desde_el_admin(admin_client, usuario):
    respuesta = admin_client.post(
        "/admin/gestorcar/vehiculo/add/",
        {**DATOS, "usuario": usuario.pk, "placa": "def-456", "estado": "activo"},
    )

    assert respuesta.status_code == 302, respuesta.context["adminform"].form.errors
    assert Vehiculo.objects.get(usuario=usuario).placa == "DEF456"


def test_listado_del_admin_filtra_por_estado_y_tipo(admin_client, vehiculo):
    respuesta = admin_client.get("/admin/gestorcar/vehiculo/?estado=activo&tipo=automovil")

    assert respuesta.status_code == 200
    assert "ABC123" in respuesta.content.decode()


def test_clean_normaliza_la_placa(usuario):
    vehiculo = Vehiculo(usuario=usuario, placa="xyz-987", **DATOS)

    vehiculo.full_clean()

    assert vehiculo.placa == "XYZ987"


def test_admin_rechaza_placa_repetida_con_mensaje(admin_client, vehiculo):
    respuesta = admin_client.post(
        "/admin/gestorcar/vehiculo/add/",
        {**DATOS, "usuario": vehiculo.usuario.pk, "placa": "abc 123", "estado": "activo"},
    )

    assert respuesta.status_code == 200
    assert "Ya tienes un vehículo registrado con esta placa." in respuesta.content.decode()
    assert Vehiculo.objects.count() == 1

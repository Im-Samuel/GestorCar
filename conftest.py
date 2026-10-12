"""Fixtures compartidas por todas las pruebas del proyecto."""

import datetime
from decimal import Decimal

import pytest

from gestorcar.models import Categoria, Registro, Vehiculo


@pytest.fixture(autouse=True)
def media_temporal(settings, tmp_path):
    """Los archivos subidos en las pruebas se guardan en una carpeta temporal."""
    settings.MEDIA_ROOT = tmp_path / "media"


@pytest.fixture
def usuario(django_user_model):
    return django_user_model.objects.create_user(
        email="ana@correo.com", password="Clave-Segura-2026", first_name="Ana", last_name="Pérez"
    )


@pytest.fixture
def otro_usuario(django_user_model):
    return django_user_model.objects.create_user(
        email="luis@correo.com", password="Clave-Segura-2026", first_name="Luis", last_name="Gómez"
    )


@pytest.fixture
def vehiculo(usuario):
    return Vehiculo.objects.create(
        usuario=usuario,
        marca="Mazda",
        modelo="3",
        anio=2018,
        placa="ABC123",
        kilometraje=50000,
        tipo=Vehiculo.Tipo.AUTOMOVIL,
    )


@pytest.fixture
def categoria():
    return Categoria.objects.create(
        nombre="Cambio de aceite", tipo_actividad=Categoria.TipoActividad.MANTENIMIENTO
    )


@pytest.fixture
def registro(vehiculo, categoria):
    return Registro.objects.create(
        vehiculo=vehiculo,
        categoria=categoria,
        fecha=datetime.date(2026, 1, 15),
        descripcion="Cambio de aceite y filtro",
        costo=Decimal("180000.00"),
        kilometraje=50000,
    )

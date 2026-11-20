"""Requisitos sobre categorías, registros, evidencias, historial y transacciones
de la especificación `integridad-datos`."""

import datetime
from decimal import Decimal

import pytest
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import DataError, IntegrityError, transaction
from django.db.models import ProtectedError

from gestorcar.models import Categoria, Evidencia, Registro, Vehiculo

pytestmark = pytest.mark.django_db


def datos_registro(**cambios):
    return {
        "fecha": datetime.date(2026, 2, 1),
        "descripcion": "Revisión técnico-mecánica",
        "costo": Decimal("250000.00"),
        "kilometraje": 52000,
        **cambios,
    }


def archivo_pdf(nombre="factura.pdf"):
    return SimpleUploadedFile(nombre, b"%PDF-1.4 prueba", content_type="application/pdf")


# Categoría con tipo de actividad


def test_categoria_duplicada_es_rechazada(categoria):
    with pytest.raises(IntegrityError), transaction.atomic():
        Categoria.objects.create(
            nombre=categoria.nombre, tipo_actividad=Categoria.TipoActividad.OTRO
        )


# Registro pertenece a un vehículo y a una categoría


def test_registro_sin_vehiculo_es_rechazado(categoria):
    with pytest.raises(IntegrityError), transaction.atomic():
        Registro.objects.create(vehiculo=None, categoria=categoria, **datos_registro())


def test_registro_sin_categoria_es_rechazado(vehiculo):
    with pytest.raises(IntegrityError), transaction.atomic():
        Registro.objects.create(vehiculo=vehiculo, categoria=None, **datos_registro())


# Valores numéricos válidos


def test_costo_negativo_es_rechazado(vehiculo, categoria):
    with pytest.raises(IntegrityError), transaction.atomic():
        Registro.objects.create(
            vehiculo=vehiculo, categoria=categoria, **datos_registro(costo=Decimal("-1"))
        )


def test_kilometraje_negativo_en_registro_es_rechazado(vehiculo, categoria):
    with pytest.raises(IntegrityError), transaction.atomic():
        Registro.objects.create(
            vehiculo=vehiculo, categoria=categoria, **datos_registro(kilometraje=-1)
        )


def test_costo_cero_se_guarda(vehiculo, categoria):
    registro = Registro.objects.create(
        vehiculo=vehiculo, categoria=categoria, **datos_registro(costo=Decimal("0"))
    )

    registro.refresh_from_db()
    assert registro.costo == Decimal("0.00")


# Evidencia pertenece a un registro


def test_eliminar_un_registro_elimina_sus_evidencias(registro):
    Evidencia.objects.create(registro=registro, archivo=archivo_pdf(), tipo="factura")
    Evidencia.objects.create(registro=registro, archivo=archivo_pdf("foto.pdf"), tipo="fotografia")

    registro.delete()

    assert Evidencia.objects.count() == 0


# Historial protegido


def test_no_se_puede_eliminar_un_vehiculo_con_historial(registro):
    vehiculo = registro.vehiculo

    with pytest.raises(ProtectedError):
        vehiculo.delete()

    assert Vehiculo.objects.filter(pk=vehiculo.pk).exists()
    assert Registro.objects.filter(pk=registro.pk).exists()


def test_no_se_puede_eliminar_una_categoria_en_uso(registro):
    with pytest.raises(ProtectedError):
        registro.categoria.delete()

    assert Categoria.objects.filter(pk=registro.categoria.pk).exists()


def test_no_se_puede_eliminar_un_usuario_con_vehiculos(vehiculo):
    with pytest.raises(ProtectedError):
        vehiculo.usuario.delete()


# Operaciones atómicas


def test_las_peticiones_son_atomicas():
    assert settings.DATABASES["default"]["ATOMIC_REQUESTS"] is True


def test_fallo_a_mitad_de_una_operacion_no_deja_datos(vehiculo, categoria):
    with pytest.raises(DataError), transaction.atomic():
        nuevo = Registro.objects.create(vehiculo=vehiculo, categoria=categoria, **datos_registro())
        # Un tipo de evidencia más largo que la columna hace fallar el segundo paso.
        Evidencia.objects.create(registro=nuevo, archivo=archivo_pdf(), tipo="x" * 30)

    assert Registro.objects.count() == 0
    assert Evidencia.objects.count() == 0


# Admin


def test_crear_registro_con_evidencia_desde_el_admin(admin_client, vehiculo, categoria):
    respuesta = admin_client.post(
        "/admin/gestorcar/registro/add/",
        {
            "vehiculo": vehiculo.pk,
            "categoria": categoria.pk,
            "fecha": "2026-02-01",
            "descripcion": "Cambio de pastillas",
            "costo": "320000",
            "kilometraje": "52000",
            "evidencias-TOTAL_FORMS": "1",
            "evidencias-INITIAL_FORMS": "0",
            "evidencias-MIN_NUM_FORMS": "0",
            "evidencias-MAX_NUM_FORMS": "1000",
            "evidencias-0-archivo": archivo_pdf(),
            "evidencias-0-tipo": "factura",
            "evidencias-0-nombre_original": "factura.pdf",
        },
    )

    assert respuesta.status_code == 302, respuesta.content.decode()[:2000]
    registro = Registro.objects.get()
    assert registro.evidencias.get().tipo == "factura"

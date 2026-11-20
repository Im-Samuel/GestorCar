"""Tests de ISSUE-006: adjuntar, consultar y eliminar evidencias."""

import io

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from gestorcar.models import Evidencia

pytestmark = pytest.mark.django_db


def url_crear(vehiculo, registro):
    return reverse("evidencias:crear", kwargs={"vehiculo_pk": vehiculo.pk, "registro_pk": registro.pk})


def url_descargar(vehiculo, registro, evidencia):
    return reverse(
        "evidencias:descargar",
        kwargs={"vehiculo_pk": vehiculo.pk, "registro_pk": registro.pk, "pk": evidencia.pk},
    )


def url_eliminar(vehiculo, registro, evidencia):
    return reverse(
        "evidencias:eliminar",
        kwargs={"vehiculo_pk": vehiculo.pk, "registro_pk": registro.pk, "pk": evidencia.pk},
    )


def archivo_pdf(nombre="factura.pdf", size=1024):
    contenido = b"%PDF-1.4 " + b"x" * size
    return SimpleUploadedFile(nombre, contenido, content_type="application/pdf")


def archivo_jpg(nombre="foto.jpg"):
    return SimpleUploadedFile(nombre, b"\xff\xd8\xff" + b"x" * 100, content_type="image/jpeg")


@pytest.fixture
def cliente(client, usuario):
    client.force_login(usuario)
    return client


@pytest.fixture
def evidencia(registro, settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path / "media"
    archivo = archivo_pdf()
    ev = Evidencia.objects.create(
        registro=registro,
        archivo=archivo,
        tipo=Evidencia.Tipo.FACTURA,
        nombre_original="factura.pdf",
    )
    return ev


# ── Subir evidencia ───────────────────────────────────────────────────────────

def test_subir_pdf_valido(cliente, vehiculo, registro):
    respuesta = cliente.post(
        url_crear(vehiculo, registro),
        {"tipo": Evidencia.Tipo.FACTURA, "archivo": archivo_pdf()},
        follow=True,
    )
    assert Evidencia.objects.count() == 1
    ev = Evidencia.objects.get()
    assert ev.nombre_original == "factura.pdf"
    assert ev.registro == registro


def test_subir_jpg_valido(cliente, vehiculo, registro):
    respuesta = cliente.post(
        url_crear(vehiculo, registro),
        {"tipo": Evidencia.Tipo.FOTOGRAFIA, "archivo": archivo_jpg()},
    )
    assert Evidencia.objects.count() == 1


def test_formato_no_permitido_es_rechazado(cliente, vehiculo, registro):
    exe = SimpleUploadedFile("virus.exe", b"MZ" + b"\x00" * 100, content_type="application/octet-stream")
    cliente.post(url_crear(vehiculo, registro), {"tipo": Evidencia.Tipo.FACTURA, "archivo": exe})
    assert Evidencia.objects.count() == 0


def test_archivo_demasiado_grande_es_rechazado(cliente, vehiculo, registro):
    from gestorcar.forms.evidencias import TAMANO_MAXIMO_BYTES
    grande = SimpleUploadedFile("grande.pdf", b"x" * (TAMANO_MAXIMO_BYTES + 1), content_type="application/pdf")
    cliente.post(url_crear(vehiculo, registro), {"tipo": Evidencia.Tipo.FACTURA, "archivo": grande})
    assert Evidencia.objects.count() == 0


def test_subir_en_registro_ajeno_devuelve_404(client, otro_usuario, vehiculo, registro):
    client.force_login(otro_usuario)
    respuesta = client.post(
        url_crear(vehiculo, registro),
        {"tipo": Evidencia.Tipo.FACTURA, "archivo": archivo_pdf()},
    )
    assert respuesta.status_code == 404


# ── Descargar evidencia ───────────────────────────────────────────────────────

def test_descargar_evidencia_propia(cliente, vehiculo, registro, evidencia):
    respuesta = cliente.get(url_descargar(vehiculo, registro, evidencia))
    assert respuesta.status_code == 200


def test_descargar_evidencia_ajena_devuelve_404(client, otro_usuario, vehiculo, registro, evidencia):
    client.force_login(otro_usuario)
    respuesta = client.get(url_descargar(vehiculo, registro, evidencia))
    assert respuesta.status_code == 404


# ── Eliminar evidencia ────────────────────────────────────────────────────────

def test_eliminar_evidencia_propia(cliente, vehiculo, registro, evidencia):
    respuesta = cliente.post(url_eliminar(vehiculo, registro, evidencia), follow=True)
    assert Evidencia.objects.count() == 0


def test_eliminar_evidencia_ajena_devuelve_404(client, otro_usuario, vehiculo, registro, evidencia):
    client.force_login(otro_usuario)
    respuesta = client.post(url_eliminar(vehiculo, registro, evidencia))
    assert respuesta.status_code == 404
    assert Evidencia.objects.count() == 1

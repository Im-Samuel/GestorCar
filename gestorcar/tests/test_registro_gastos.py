"""
Tests de ISSUE-005 e ISSUE-007: registro, edición y eliminación de gastos.
"""

import datetime
from decimal import Decimal

import pytest
from django.urls import reverse

from gestorcar.models import Registro

pytestmark = pytest.mark.django_db


def url_lista(vehiculo):
    return reverse("registros:lista", kwargs={"vehiculo_pk": vehiculo.pk})


def url_crear(vehiculo):
    return reverse("registros:crear", kwargs={"vehiculo_pk": vehiculo.pk})


def url_detalle(vehiculo, registro):
    return reverse("registros:detalle", kwargs={"vehiculo_pk": vehiculo.pk, "pk": registro.pk})


def url_editar(vehiculo, registro):
    return reverse("registros:editar", kwargs={"vehiculo_pk": vehiculo.pk, "pk": registro.pk})


def url_eliminar(vehiculo, registro):
    return reverse("registros:eliminar", kwargs={"vehiculo_pk": vehiculo.pk, "pk": registro.pk})


def datos_validos(categoria, **cambios):
    return {
        "fecha": "2026-06-01",
        "categoria": categoria.pk,
        "descripcion": "Cambio de aceite completo",
        "costo": "180000.00",
        "kilometraje": "52000",
        **cambios,
    }


@pytest.fixture
def cliente(client, usuario):
    client.force_login(usuario)
    return client


# ── Lista y visibilidad ────────────────────────────────────────────────────────

def test_lista_requiere_autenticacion(client, vehiculo):
    respuesta = client.get(url_lista(vehiculo))
    assert respuesta.status_code == 302
    assert "iniciar-sesion" in respuesta["Location"]


def test_lista_muestra_registros_del_vehiculo(cliente, vehiculo, registro):
    respuesta = cliente.get(url_lista(vehiculo))
    assert respuesta.status_code == 200
    assert registro in respuesta.context["registros"]


def test_lista_no_muestra_registros_de_otro_usuario(cliente, otro_usuario, django_user_model, categoria):
    otro = django_user_model.objects.create_user(
        email="otro@correo.com", password="x", first_name="X", last_name="Y"
    )
    from gestorcar.models import Vehiculo
    otro_vehiculo = Vehiculo.objects.create(
        usuario=otro, marca="Ford", modelo="Ka", anio=2019,
        placa="ZZZ111", kilometraje=10000, tipo=Vehiculo.Tipo.AUTOMOVIL,
    )
    # La lista del vehículo de otro usuario devuelve 404 al usuario autenticado.
    respuesta = cliente.get(url_lista(otro_vehiculo))
    assert respuesta.status_code == 404


# ── Crear registro válido ─────────────────────────────────────────────────────

def test_crear_registro_valido(cliente, vehiculo, categoria):
    respuesta = cliente.post(url_crear(vehiculo), datos_validos(categoria), follow=True)

    assert Registro.objects.count() == 1
    registro = Registro.objects.get()
    assert registro.vehiculo == vehiculo
    assert registro.costo == Decimal("180000.00")
    assert registro.kilometraje == 52000
    assert respuesta.redirect_chain[-1][0] == url_detalle(vehiculo, registro)


def test_crear_registro_en_vehiculo_ajeno_devuelve_404(client, otro_usuario, vehiculo, categoria):
    client.force_login(otro_usuario)
    respuesta = client.post(url_crear(vehiculo), datos_validos(categoria))
    assert respuesta.status_code == 404


# ── Validaciones de creación ──────────────────────────────────────────────────

def test_fecha_futura_es_invalida(cliente, vehiculo, categoria):
    respuesta = cliente.post(url_crear(vehiculo), datos_validos(categoria, fecha="2099-01-01"))
    assert respuesta.status_code == 200
    assert "fecha" in respuesta.context["form"].errors
    assert Registro.objects.count() == 0


def test_costo_negativo_es_invalido(cliente, vehiculo, categoria):
    respuesta = cliente.post(url_crear(vehiculo), datos_validos(categoria, costo="-100"))
    assert respuesta.status_code == 200
    assert "costo" in respuesta.context["form"].errors
    assert Registro.objects.count() == 0


def test_kilometraje_vacio_es_invalido(cliente, vehiculo, categoria):
    respuesta = cliente.post(url_crear(vehiculo), datos_validos(categoria, kilometraje=""))
    assert respuesta.status_code == 200
    assert "kilometraje" in respuesta.context["form"].errors
    assert Registro.objects.count() == 0


def test_descripcion_vacia_es_invalida(cliente, vehiculo, categoria):
    respuesta = cliente.post(url_crear(vehiculo), datos_validos(categoria, descripcion=""))
    assert respuesta.status_code == 200
    assert "descripcion" in respuesta.context["form"].errors
    assert Registro.objects.count() == 0


def test_categoria_obligatoria(cliente, vehiculo, categoria):
    datos = datos_validos(categoria)
    datos.pop("categoria")
    respuesta = cliente.post(url_crear(vehiculo), datos)
    assert respuesta.status_code == 200
    assert "categoria" in respuesta.context["form"].errors
    assert Registro.objects.count() == 0


# ── Editar registro ───────────────────────────────────────────────────────────

def test_editar_registro_actualiza_datos(cliente, vehiculo, registro, categoria):
    respuesta = cliente.post(
        url_editar(vehiculo, registro),
        datos_validos(categoria, descripcion="Descripción actualizada", costo="200000"),
        follow=True,
    )
    registro.refresh_from_db()
    assert registro.descripcion == "Descripción actualizada"
    assert registro.costo == Decimal("200000")
    assert respuesta.redirect_chain[-1][0] == url_detalle(vehiculo, registro)


def test_editar_registro_ajeno_devuelve_404(client, otro_usuario, vehiculo, registro, categoria):
    client.force_login(otro_usuario)
    respuesta = client.post(url_editar(vehiculo, registro), datos_validos(categoria))
    assert respuesta.status_code == 404


# ── Eliminar registro ─────────────────────────────────────────────────────────

def test_get_eliminar_muestra_confirmacion(cliente, vehiculo, registro):
    respuesta = cliente.get(url_eliminar(vehiculo, registro))
    assert respuesta.status_code == 200
    assert "confirmar_eliminacion" in respuesta.templates[0].name


def test_post_eliminar_borra_el_registro(cliente, vehiculo, registro):
    respuesta = cliente.post(url_eliminar(vehiculo, registro), follow=True)
    assert Registro.objects.count() == 0
    assert respuesta.redirect_chain[-1][0] == url_lista(vehiculo)


def test_eliminar_registro_ajeno_devuelve_404(client, otro_usuario, vehiculo, registro):
    client.force_login(otro_usuario)
    respuesta = client.post(url_eliminar(vehiculo, registro))
    assert respuesta.status_code == 404
    assert Registro.objects.count() == 1

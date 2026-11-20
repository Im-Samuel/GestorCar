"""Escenarios de la especificación `gestion-vehiculos`."""

import pytest
from django.core.exceptions import ValidationError
from django.urls import URLPattern, URLResolver, get_resolver, reverse
from django.utils import timezone

from gestorcar.models import Registro, Vehiculo

pytestmark = pytest.mark.django_db

LISTA = reverse("vehiculos:lista")
CREAR = reverse("vehiculos:crear")


def detalle(vehiculo):
    return reverse("vehiculos:detalle", args=[vehiculo.pk])


def editar(vehiculo):
    return reverse("vehiculos:editar", args=[vehiculo.pk])


def retirar(vehiculo):
    return reverse("vehiculos:retirar", args=[vehiculo.pk])


def datos(**cambios):
    return {
        "marca": "Renault",
        "modelo": "Logan",
        "anio": "2020",
        "placa": "XYZ987",
        "kilometraje": "30000",
        "tipo": "automovil",
        **cambios,
    }


def errores(respuesta, campo):
    return respuesta.context["form"].errors.get(campo, [])


@pytest.fixture
def cliente(client, usuario):
    client.force_login(usuario)
    return client


# Registrar vehículo


def test_registro_valido_queda_del_usuario_y_activo(cliente, usuario):
    respuesta = cliente.post(CREAR, datos(), follow=True)

    vehiculo = Vehiculo.objects.get()
    assert vehiculo.usuario == usuario
    assert vehiculo.estado == Vehiculo.Estado.ACTIVO
    assert respuesta.redirect_chain == [(detalle(vehiculo), 302)]
    html = respuesta.content.decode()
    assert "Vehículo registrado." in html
    assert "XYZ987" in html


def test_varios_vehiculos_aparecen_en_el_listado(cliente):
    cliente.post(CREAR, datos())
    cliente.post(CREAR, datos(marca="Mazda", modelo="CX-5", placa="JKL456"))

    html = cliente.get(LISTA).content.decode()

    assert Vehiculo.objects.count() == 2
    assert "XYZ987" in html and "JKL456" in html


# Validar datos del vehículo


def test_placa_repetida_muestra_error_en_el_campo_placa(cliente, vehiculo):
    respuesta = cliente.post(CREAR, datos(placa="abc 123"))

    assert respuesta.status_code == 200
    assert errores(respuesta, "placa") == ["Ya tienes un vehículo registrado con esta placa."]
    assert Vehiculo.objects.count() == 1


@pytest.mark.parametrize("desfase", [-1, 2])
def test_anio_fuera_de_rango_muestra_error_en_el_campo_anio(cliente, desfase):
    anio = 1899 if desfase < 0 else timezone.localdate().year + desfase

    respuesta = cliente.post(CREAR, datos(anio=str(anio)))

    assert errores(respuesta, "anio")
    assert not Vehiculo.objects.exists()


def test_anio_siguiente_al_actual_se_acepta(cliente):
    cliente.post(CREAR, datos(anio=str(timezone.localdate().year + 1)))

    assert Vehiculo.objects.count() == 1


def test_kilometraje_negativo_muestra_error_en_el_campo_kilometraje(cliente):
    respuesta = cliente.post(CREAR, datos(kilometraje="-10"))

    assert errores(respuesta, "kilometraje")
    assert not Vehiculo.objects.exists()


def test_campos_obligatorios_vacios(cliente):
    respuesta = cliente.post(CREAR, {})

    for campo in ("marca", "modelo", "anio", "placa", "kilometraje", "tipo"):
        assert errores(respuesta, campo), campo
    assert not Vehiculo.objects.exists()


def test_validacion_fuera_del_formulario(usuario):
    vehiculo = Vehiculo(
        usuario=usuario,
        marca="Ford",
        modelo="T",
        anio=1800,
        placa="AAA111",
        kilometraje=0,
        tipo="automovil",
    )

    with pytest.raises(ValidationError) as error:
        vehiculo.full_clean()

    assert error.value.message_dict == {"anio": ["El año debe ser 1900 o posterior."]}


# Consultar vehículos propios


def test_listado_muestra_primero_los_activos_y_marca_los_retirados(cliente, usuario):
    retirado = Vehiculo.objects.create(
        usuario=usuario, marca="Audi", modelo="A4", anio=2010, placa="RET111",
        kilometraje=200000, tipo="automovil", estado=Vehiculo.Estado.RETIRADO,
    )  # fmt: skip
    activo = Vehiculo.objects.create(
        usuario=usuario, marca="Toyota", modelo="Hilux", anio=2022, placa="ACT222",
        kilometraje=10000, tipo="camioneta",
    )  # fmt: skip

    respuesta = cliente.get(LISTA)

    assert list(respuesta.context["vehiculos"]) == [activo, retirado]
    assert '<span class="insignia insignia-retirado">Retirado</span>' in respuesta.content.decode()


def test_sin_vehiculos_ofrece_registrar_uno(cliente):
    html = cliente.get(LISTA).content.decode()

    assert "Todavía no tienes vehículos registrados." in html
    assert f'href="{CREAR}"' in html


def test_la_pagina_de_inicio_muestra_el_listado(cliente, vehiculo):
    respuesta = cliente.get(reverse("inicio"), follow=True)

    assert respuesta.redirect_chain == [(LISTA, 302)]
    assert vehiculo.placa in respuesta.content.decode()


def test_el_detalle_muestra_los_datos(cliente, vehiculo):
    html = cliente.get(detalle(vehiculo)).content.decode()

    for dato in ("Mazda", "ABC123", "2018", "50000 km", "Automóvil", "Activo"):
        assert dato in html, dato


def test_la_barra_de_navegacion_tiene_mis_vehiculos(cliente):
    html = cliente.get(LISTA).content.decode()

    assert f'href="{LISTA}" aria-current="page">Mis vehículos</a>' in html


# Actualizar vehículo


def test_formulario_de_edicion_precargado(cliente, vehiculo):
    formulario = cliente.get(editar(vehiculo)).context["form"]

    assert formulario.initial["placa"] == "ABC123"
    assert formulario.initial["kilometraje"] == 50000


def test_actualizar_kilometraje_conserva_los_registros(cliente, vehiculo, registro):
    respuesta = cliente.post(
        editar(vehiculo),
        datos(marca="Mazda", modelo="3", anio="2018", placa="ABC123", kilometraje="52000"),
        follow=True,
    )

    vehiculo.refresh_from_db()
    assert vehiculo.kilometraje == 52000
    assert "52000 km" in respuesta.content.decode()
    assert list(vehiculo.registros.all()) == [registro]
    registro.refresh_from_db()
    assert registro.kilometraje == 50000


def test_editar_conservando_la_misma_placa_no_es_placa_repetida(cliente, vehiculo):
    respuesta = cliente.post(editar(vehiculo), datos(placa="abc-123"))

    assert respuesta.status_code == 302


# Retirar vehículo


def test_retiro_confirmado_conserva_el_historial(cliente, vehiculo, registro):
    respuesta = cliente.post(retirar(vehiculo), follow=True)

    vehiculo.refresh_from_db()
    assert vehiculo.estado == Vehiculo.Estado.RETIRADO
    assert respuesta.redirect_chain == [(detalle(vehiculo), 302)]
    assert "Vehículo retirado. Su historial se conserva." in respuesta.content.decode()
    assert Registro.objects.filter(vehiculo=vehiculo).count() == 1


def test_abrir_el_retiro_y_cancelar_no_cambia_nada(cliente, vehiculo):
    html = cliente.get(retirar(vehiculo)).content.decode()

    vehiculo.refresh_from_db()
    assert vehiculo.estado == Vehiculo.Estado.ACTIVO
    assert f'href="{detalle(vehiculo)}" class="btn btn-secundario">Cancelar' in html


def test_retirar_dos_veces_no_tiene_efecto(cliente, vehiculo):
    cliente.post(retirar(vehiculo))
    respuesta = cliente.post(retirar(vehiculo), follow=True)

    assert "Este vehículo ya estaba retirado." in respuesta.content.decode()


def test_un_retirado_sigue_consultable_y_sin_boton_de_retirar(cliente, vehiculo):
    cliente.post(retirar(vehiculo))

    html = cliente.get(detalle(vehiculo)).content.decode()

    assert "Retirado" in html
    assert retirar(vehiculo) not in html


def test_no_existe_ninguna_url_para_eliminar_vehiculos(cliente, vehiculo):
    def nombres(patrones, prefijo=""):
        for p in patrones:
            if isinstance(p, URLResolver):
                yield from nombres(p.url_patterns, prefijo + str(p.pattern))
            elif isinstance(p, URLPattern):
                yield prefijo + str(p.pattern), p.name or ""

    rutas_vehiculos = [r for r in nombres(get_resolver().url_patterns) if "vehiculos/" in r[0]]

    assert rutas_vehiculos
    assert not [r for r in rutas_vehiculos if "elimin" in r[0] + r[1] or "borr" in r[0] + r[1]]
    for url in (LISTA, detalle(vehiculo), editar(vehiculo)):
        html = cliente.get(url).content.decode().lower()
        assert "eliminar" not in html and "borrar" not in html


# Vehículos de otros usuarios


@pytest.mark.parametrize("pagina", [detalle, editar, retirar])
def test_vehiculo_ajeno_responde_no_encontrado(client, vehiculo, otro_usuario, pagina):
    client.force_login(otro_usuario)

    assert client.get(pagina(vehiculo)).status_code == 404
    if pagina is not detalle:  # El detalle solo acepta GET.
        assert client.post(pagina(vehiculo), datos(kilometraje="1")).status_code == 404

    vehiculo.refresh_from_db()
    assert vehiculo.estado == Vehiculo.Estado.ACTIVO
    assert vehiculo.kilometraje == 50000


def test_cada_usuario_ve_solo_sus_vehiculos(client, vehiculo, otro_usuario):
    propio = Vehiculo.objects.create(
        usuario=otro_usuario, marca="Kia", modelo="Rio", anio=2019, placa="OTR999",
        kilometraje=1000, tipo="automovil",
    )  # fmt: skip
    client.force_login(otro_usuario)

    vehiculos = list(client.get(LISTA).context["vehiculos"])

    assert vehiculos == [propio]

"""Escenarios de la especificación `autenticacion`."""

import pytest
from django.urls import reverse

from gestorcar.models import Usuario, Vehiculo

pytestmark = pytest.mark.django_db

REGISTRO = reverse("cuentas:registro")
INICIAR_SESION = reverse("cuentas:iniciar_sesion")
CERRAR_SESION = reverse("cuentas:cerrar_sesion")
INICIO = reverse("inicio")
CLAVE = "Clave-Segura-2026"  # La de las fixtures `usuario` y `otro_usuario`.


def datos_registro(**cambios):
    return {
        "first_name": "Marta",
        "last_name": "Ríos",
        "email": "marta@correo.com",
        "password1": "Una-Clave-Larga-2026",
        "password2": "Una-Clave-Larga-2026",
        **cambios,
    }


def errores(respuesta, campo):
    return respuesta.context["form"].errors.get(campo, [])


# Registro de cuenta


def test_registro_exitoso_crea_la_cuenta_e_inicia_sesion(client):
    respuesta = client.post(REGISTRO, datos_registro(), follow=True)

    # Inicio lleva al listado de vehículos.
    assert respuesta.redirect_chain == [(INICIO, 302), (reverse("vehiculos:lista"), 302)]
    usuario = Usuario.objects.get(email="marta@correo.com")
    assert respuesta.context["user"] == usuario
    assert "¡Bienvenido a GestorCar, Marta!" in respuesta.content.decode()


def test_correo_ya_registrado_muestra_error_en_el_campo_correo(client, usuario):
    respuesta = client.post(REGISTRO, datos_registro(email="ANA@Correo.com"))

    assert respuesta.status_code == 200
    assert errores(respuesta, "email") == ["Ya existe una cuenta con este correo electrónico."]
    assert Usuario.objects.count() == 1


def test_contrasenas_distintas_muestran_error_en_la_confirmacion(client):
    respuesta = client.post(REGISTRO, datos_registro(password2="Otra-Clave-2026"))

    assert errores(respuesta, "password2")
    assert not Usuario.objects.exists()


@pytest.mark.parametrize(
    "clave",
    ["corta1", "password123", "12345678901", "marta@correo.co"],
    ids=["corta", "comun", "solo-numeros", "parecida-a-los-datos"],
)
def test_contrasena_debil_muestra_el_motivo_en_el_campo_contrasena(client, clave):
    respuesta = client.post(REGISTRO, datos_registro(password1=clave, password2=clave))

    assert errores(respuesta, "password1")
    assert not errores(respuesta, "password2")
    assert not Usuario.objects.exists()


def test_campos_obligatorios_vacios_muestran_error_en_cada_campo(client):
    respuesta = client.post(REGISTRO, {})

    for campo in ("first_name", "last_name", "email", "password1", "password2"):
        assert errores(respuesta, campo) == ["Este campo es obligatorio."], campo
    assert not Usuario.objects.exists()


# Inicio de sesión


def test_credenciales_validas_inician_sesion_y_llevan_a_inicio(client, usuario):
    respuesta = client.post(INICIAR_SESION, {"username": "ana@correo.com", "password": CLAVE})

    assert respuesta.status_code == 302
    assert respuesta.url == INICIO


def test_credenciales_invalidas_muestran_el_mismo_mensaje_en_ambos_casos(client, usuario):
    correo_inexistente = client.post(
        INICIAR_SESION, {"username": "nadie@correo.com", "password": CLAVE}
    )
    clave_incorrecta = client.post(
        INICIAR_SESION, {"username": "ana@correo.com", "password": "No-Es-La-Clave"}
    )

    mensaje = correo_inexistente.context["form"].non_field_errors()
    assert mensaje
    assert mensaje == clave_incorrecta.context["form"].non_field_errors()
    assert "_auth_user_id" not in client.session


@pytest.mark.urls("gestorcar.tests.urls_prueba")
def test_regreso_a_la_pagina_solicitada_tras_iniciar_sesion(client, usuario):
    destino = "/prueba/vista-nueva/"
    redireccion = client.get(destino)
    assert redireccion.url == f"{INICIAR_SESION}?next={destino}"

    respuesta = client.post(
        INICIAR_SESION, {"username": "ana@correo.com", "password": CLAVE, "next": destino}
    )

    assert respuesta.url == destino


# Cierre de sesión


def test_cerrar_sesion_lleva_a_iniciar_sesion(client, usuario):
    client.force_login(usuario)

    respuesta = client.post(CERRAR_SESION)

    assert respuesta.url == INICIAR_SESION
    assert "_auth_user_id" not in client.session


def test_pagina_protegida_despues_de_salir_pide_iniciar_sesion(client, usuario):
    client.force_login(usuario)
    client.post(CERRAR_SESION)

    respuesta = client.get(INICIO)

    assert respuesta.status_code == 302
    assert respuesta.url.startswith(INICIAR_SESION)


def test_cerrar_sesion_no_acepta_get(client, usuario):
    client.force_login(usuario)

    assert client.get(CERRAR_SESION).status_code == 405
    assert "_auth_user_id" in client.session


def test_la_barra_de_navegacion_tiene_el_boton_de_cerrar_sesion(client, usuario):
    client.force_login(usuario)

    html = client.get(INICIO, follow=True).content.decode()

    assert f'action="{CERRAR_SESION}"' in html
    assert "Cerrar sesión" in html
    assert "Ana Pérez" in html


# Acceso protegido por defecto


def test_inicio_con_sesion_muestra_la_barra_con_el_usuario(client, usuario):
    client.force_login(usuario)

    respuesta = client.get(INICIO, follow=True)

    assert respuesta.status_code == 200
    assert "Ana Pérez" in respuesta.content.decode()


def test_inicio_sin_sesion_redirige_a_iniciar_sesion(client):
    respuesta = client.get(INICIO)

    assert respuesta.url == f"{INICIAR_SESION}?next={INICIO}"


@pytest.mark.urls("gestorcar.tests.urls_prueba")
def test_pagina_nueva_sin_configuracion_adicional_exige_sesion(client, usuario):
    sin_sesion = client.get("/prueba/vista-nueva/")
    client.force_login(usuario)
    con_sesion = client.get("/prueba/vista-nueva/")

    assert sin_sesion.status_code == 302
    assert sin_sesion.url.startswith(INICIAR_SESION)
    assert con_sesion.content == b"contenido privado"


@pytest.mark.parametrize("pagina", [REGISTRO, INICIAR_SESION])
def test_usuario_con_sesion_que_abre_registro_o_inicio_de_sesion_va_a_inicio(
    client, usuario, pagina
):
    client.force_login(usuario)

    respuesta = client.get(pagina)

    assert respuesta.status_code == 302
    assert respuesta.url == INICIO


def test_registro_e_inicio_de_sesion_son_accesibles_sin_sesion(client):
    assert client.get(REGISTRO).status_code == 200
    assert client.get(INICIAR_SESION).status_code == 200
    assert client.get("/admin/login/").status_code == 200


# Aislamiento entre cuentas


@pytest.mark.urls("gestorcar.tests.urls_prueba")
def test_dato_de_otra_cuenta_responde_no_encontrado(client, vehiculo, otro_usuario):
    client.force_login(otro_usuario)

    respuesta = client.get(f"/prueba/vehiculos/{vehiculo.pk}/")

    assert respuesta.status_code == 404
    assert vehiculo.placa not in respuesta.content.decode()


@pytest.mark.urls("gestorcar.tests.urls_prueba")
def test_el_dueno_si_ve_su_dato(client, vehiculo):
    client.force_login(vehiculo.usuario)

    respuesta = client.get(f"/prueba/vehiculos/{vehiculo.pk}/")

    assert respuesta.content.decode() == vehiculo.placa
    assert Vehiculo.objects.count() == 1


# Formularios comprensibles y accesibles


def test_error_asociado_al_campo_para_lectores_de_pantalla(client):
    html = client.post(REGISTRO, datos_registro(email="no-es-un-correo")).content.decode()

    assert 'aria-invalid="true"' in html
    assert 'aria-describedby="id_email_error"' in html
    assert 'id="id_email_error"' in html
    assert "Introduzca una dirección de correo electrónico válida." in html


def test_ayuda_de_la_contrasena_enlazada_al_campo(client):
    html = client.get(REGISTRO).content.decode()

    assert 'aria-describedby="id_password1_helptext"' in html
    assert 'id="id_password1_helptext"' in html


def test_los_formularios_marcan_los_campos_obligatorios(client):
    html = client.get(REGISTRO).content.decode()

    assert html.count('aria-hidden="true">*</span>') >= 5
    assert "son obligatorios" in html


def test_el_registro_empieza_por_el_primer_campo(client):
    html = client.get(REGISTRO).content.decode()

    assert html.count("autofocus") == 1
    assert 'name="first_name"' in html.split("autofocus")[0].rsplit("<input", 1)[1]

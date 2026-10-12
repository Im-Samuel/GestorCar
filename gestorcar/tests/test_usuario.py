"""Requisito "Usuario identificado por correo" de la especificación `integridad-datos`."""

import pytest
from django.core.management import call_command
from django.db import IntegrityError, transaction

from gestorcar.models import Usuario

pytestmark = pytest.mark.django_db


def test_correo_repetido_con_distinta_capitalizacion_es_rechazado(usuario):
    # Directamente en la base de datos, sin la normalización del manager.
    with pytest.raises(IntegrityError), transaction.atomic():
        Usuario.objects.create(email="Ana@Correo.com", first_name="Ana", last_name="Otra")

    # Y a través del manager, que normaliza el correo antes de guardar.
    with pytest.raises(IntegrityError), transaction.atomic():
        Usuario.objects.create_user(email="ANA@correo.com", password="x")

    assert Usuario.objects.count() == 1


def test_contrasena_se_guarda_como_hash():
    usuario = Usuario.objects.create_user(email="bea@correo.com", password="Secreta-2026")

    assert "Secreta-2026" not in usuario.password
    assert usuario.password.startswith("pbkdf2_sha256$")
    assert usuario.check_password("Secreta-2026")


def test_el_correo_se_guarda_en_minusculas():
    usuario = Usuario.objects.create_user(email="Carla@Correo.COM", password="x")

    assert usuario.email == "carla@correo.com"


def test_inicio_de_sesion_ignora_mayusculas_del_correo(usuario):
    assert Usuario.objects.get_by_natural_key("ANA@CORREO.COM") == usuario


def test_el_usuario_no_tiene_nombre_de_usuario():
    campos = {campo.name for campo in Usuario._meta.get_fields()}

    assert "username" not in campos
    assert Usuario.USERNAME_FIELD == "email"


def test_createsuperuser_usa_correo_en_lugar_de_nombre_de_usuario(monkeypatch):
    monkeypatch.setenv("DJANGO_SUPERUSER_PASSWORD", "Admin-Segura-2026")

    call_command(
        "createsuperuser",
        interactive=False,
        email="Admin@Correo.com",
        first_name="Admin",
        last_name="GestorCar",
        verbosity=0,
    )

    admin = Usuario.objects.get(email="admin@correo.com")
    assert admin.is_superuser and admin.is_staff


def test_crear_usuario_desde_el_admin(admin_client):
    respuesta = admin_client.post(
        "/admin/gestorcar/usuario/add/",
        {
            "email": "nuevo@correo.com",
            "first_name": "Nuevo",
            "last_name": "Usuario",
            "usable_password": "true",
            "password1": "Clave-Segura-2026",
            "password2": "Clave-Segura-2026",
        },
    )

    assert respuesta.status_code == 302, respuesta.context["adminform"].form.errors
    assert Usuario.objects.filter(email="nuevo@correo.com").exists()


def test_admin_rechaza_correo_repetido_con_mensaje(admin_client, usuario):
    respuesta = admin_client.post(
        "/admin/gestorcar/usuario/add/",
        {
            "email": "ANA@correo.com",
            "first_name": "Ana",
            "last_name": "Repetida",
            "usable_password": "true",
            "password1": "Clave-Segura-2026",
            "password2": "Clave-Segura-2026",
        },
    )

    assert respuesta.status_code == 200
    assert "Ya existe un usuario con este correo electrónico." in respuesta.content.decode()

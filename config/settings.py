"""
Configuración de Django para GestorCar.

Los valores que cambian entre equipos o entornos (secretos, depuración, hosts,
base de datos y zona horaria) se leen de variables de entorno. Ver
`.env.example` para la lista completa.

https://docs.djangoproject.com/en/5.2/topics/settings/
https://docs.djangoproject.com/en/5.2/ref/settings/
"""

import os
from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()

# El archivo .env es opcional: dentro de Docker las variables llegan desde
# docker-compose. DJANGO_ENV_FILE permite usar otro archivo (lo usan las pruebas).
ENV_FILE = Path(os.environ.get("DJANGO_ENV_FILE", BASE_DIR / ".env"))
if ENV_FILE.is_file():
    env.read_env(ENV_FILE)


# Seguridad
# https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# Obligatoria: sin valor por defecto, el arranque falla si no está definida.
SECRET_KEY = env("SECRET_KEY")

DEBUG = env.bool("DEBUG", default=False)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])


# Aplicaciones

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # App de GestorCar, organizada por capas MVC (ver README).
    "gestorcar",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    # Toda vista exige sesión salvo las marcadas con @login_not_required.
    "django.contrib.auth.middleware.LoginRequiredMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Modelo de usuario propio (inicio de sesión por correo). Debe definirse antes
# de la primera migración.
AUTH_USER_MODEL = "gestorcar.Usuario"

ROOT_URLCONF = "config.urls"

# Autenticación
LOGIN_URL = "cuentas:iniciar_sesion"
LOGIN_REDIRECT_URL = "inicio"
LOGOUT_REDIRECT_URL = "cuentas:iniciar_sesion"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # Plantillas HTML (la V del MVC).
        "DIRS": [BASE_DIR / "gestorcar" / "views"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Base de datos
# Obligatoria. Formato: postgres://usuario:contraseña@host:puerto/base_de_datos
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": env.db("DATABASE_URL"),
}
# Cada petición se confirma completa o se revierte entera (RNF-08).
DATABASES["default"]["ATOMIC_REQUESTS"] = True


# Validación de contraseñas
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Idioma y zona horaria
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "es"

# Las fechas se guardan en UTC (USE_TZ); TIME_ZONE solo afecta cómo se muestran.
TIME_ZONE = env("TIME_ZONE", default="UTC")

USE_I18N = True

USE_TZ = True


# Archivos estáticos (CSS, JavaScript, imágenes)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = "static/"
# CSS compilado por Tailwind (static/css/app.css) y demás archivos propios.
STATICFILES_DIRS = [BASE_DIR / "static"]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

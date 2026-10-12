"""Escenarios de la especificación `entorno-ejecucion` sobre la configuración.

Cada prueba carga `config.settings` en un proceso aparte con un entorno
controlado, porque la configuración solo se lee una vez al arrancar.
"""

import os
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
VARIABLES_CONTROLADAS = ("SECRET_KEY", "DATABASE_URL", "DEBUG")


def cargar_configuracion(tmp_path, codigo, **variables):
    """Importa `config.settings` sin `.env` y solo con las variables indicadas."""
    entorno = {k: v for k, v in os.environ.items() if k not in VARIABLES_CONTROLADAS}
    entorno["DJANGO_ENV_FILE"] = str(tmp_path / "no-existe.env")
    entorno.update(variables)
    return subprocess.run(
        [sys.executable, "-c", f"import config.settings as s; {codigo}"],
        cwd=BASE_DIR,
        env=entorno,
        capture_output=True,
        text=True,
    )


def test_sin_secret_key_el_arranque_falla_nombrando_la_variable(tmp_path):
    resultado = cargar_configuracion(
        tmp_path, "pass", DATABASE_URL="postgres://u:p@localhost:5432/db"
    )

    assert resultado.returncode != 0
    assert "SECRET_KEY" in resultado.stderr


def test_sin_database_url_el_arranque_falla_nombrando_la_variable(tmp_path):
    resultado = cargar_configuracion(tmp_path, "pass", SECRET_KEY="clave-de-prueba")

    assert resultado.returncode != 0
    assert "DATABASE_URL" in resultado.stderr


def test_debug_es_false_si_no_se_define(tmp_path):
    resultado = cargar_configuracion(
        tmp_path,
        "print(s.DEBUG)",
        SECRET_KEY="clave-de-prueba",
        DATABASE_URL="postgres://u:p@localhost:5432/db",
    )

    assert resultado.returncode == 0, resultado.stderr
    assert resultado.stdout.strip() == "False"

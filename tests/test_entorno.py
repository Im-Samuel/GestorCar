"""Prueba de humo del entorno: base de datos y migraciones."""

import pytest
from django.core.management import call_command
from django.db import connection
from django.db.migrations.executor import MigrationExecutor


@pytest.mark.django_db
def test_la_base_de_datos_es_postgresql():
    assert connection.vendor == "postgresql"


@pytest.mark.django_db
def test_no_quedan_migraciones_sin_aplicar():
    ejecutor = MigrationExecutor(connection)
    pendientes = ejecutor.migration_plan(ejecutor.loader.graph.leaf_nodes())

    assert pendientes == []


@pytest.mark.django_db
def test_los_modelos_no_tienen_cambios_sin_migracion():
    # --check termina con error si algún modelo necesita una migración nueva.
    call_command("makemigrations", "--check", "--dry-run", verbosity=0)

"""
ISSUE-004 - Catálogo inicial de categorías (RF-09).

Carga las categorías predefinidas que exige RF-09:
mantenimientos preventivos y correctivos, cambio de aceite, reparación o
reemplazo de piezas, modificaciones estéticas y mecánicas, instalación de
accesorios, revisiones, trámites, seguros, impuestos, combustible y
otro gasto relacionado.
"""

from django.db import migrations

CATEGORIAS = [
    # --- Mantenimiento ---
    ("Mantenimiento preventivo", "mantenimiento"),
    ("Mantenimiento correctivo", "mantenimiento"),
    ("Cambio de aceite", "mantenimiento"),
    ("Cambio de filtros", "mantenimiento"),
    ("Cambio de llantas", "mantenimiento"),
    ("Alineación y balanceo", "mantenimiento"),
    ("Revisión de frenos", "mantenimiento"),
    ("Revisión periódica", "mantenimiento"),
    # --- Reparación ---
    ("Reparación de motor", "reparacion"),
    ("Reparación de frenos", "reparacion"),
    ("Reparación de suspensión", "reparacion"),
    ("Reemplazo de piezas", "reparacion"),
    ("Reparación eléctrica", "reparacion"),
    ("Reparación de carrocería", "reparacion"),
    # --- Modificación ---
    ("Modificación estética", "modificacion"),
    ("Modificación mecánica", "modificacion"),
    ("Instalación de accesorios", "modificacion"),
    ("Mejoras de rendimiento", "modificacion"),
    # --- Otro ---
    ("Trámites y documentación", "otro"),
    ("Seguro vehicular", "otro"),
    ("Impuestos y tasas", "otro"),
    ("Combustible", "otro"),
    ("Lavado y detallado", "otro"),
    ("Parqueadero y peajes", "otro"),
    ("Otro gasto relacionado", "otro"),
]


def cargar_categorias(apps, schema_editor):
    Categoria = apps.get_model("gestorcar", "Categoria")
    db_alias = schema_editor.connection.alias
    Categoria.objects.using(db_alias).bulk_create(
        [Categoria(nombre=nombre, tipo_actividad=tipo) for nombre, tipo in CATEGORIAS],
        ignore_conflicts=True,
    )


def eliminar_categorias(apps, schema_editor):
    Categoria = apps.get_model("gestorcar", "Categoria")
    nombres = [nombre for nombre, _ in CATEGORIAS]
    Categoria.objects.using(schema_editor.connection.alias).filter(
        nombre__in=nombres
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("gestorcar", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(cargar_categorias, eliminar_categorias),
    ]

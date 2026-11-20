"""
Índices adicionales para RNF-10, RNF-11 (ISSUE-014).

Los filtros más comunes sobre Registro son:
  - vehiculo + fecha      → ya cubierto por registro_vehiculo_fecha_idx (0001)
  - vehiculo + categoria  → aggregaciones por categoría (ISSUE-010)
  - vehiculo + fecha + categoria → filtros combinados del historial (ISSUE-008)

El índice sobre Vehiculo(usuario) acelera la lista de vehículos y la comparación.
"""

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gestorcar", "0002_catalogo_categorias"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="registro",
            index=models.Index(
                fields=["vehiculo", "categoria"],
                name="registro_vehiculo_categoria_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="vehiculo",
            index=models.Index(
                fields=["usuario"],
                name="vehiculo_usuario_idx",
            ),
        ),
    ]

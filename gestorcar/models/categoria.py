from django.db import models


class Categoria(models.Model):
    """Categoría de un registro. El catálogo inicial se carga en ISSUE-004."""

    class TipoActividad(models.TextChoices):
        MANTENIMIENTO = "mantenimiento", "Mantenimiento"
        REPARACION = "reparacion", "Reparación"
        MODIFICACION = "modificacion", "Modificación"
        OTRO = "otro", "Otro gasto"

    nombre = models.CharField("nombre", max_length=80, unique=True)
    tipo_actividad = models.CharField(
        "tipo de actividad", max_length=20, choices=TipoActividad.choices
    )

    class Meta:
        verbose_name = "categoría"
        verbose_name_plural = "categorías"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre

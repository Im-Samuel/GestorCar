from django.db import models

from .categoria import Categoria
from .vehiculo import Vehiculo


class Registro(models.Model):
    """Gasto o intervención realizada a un vehículo."""

    vehiculo = models.ForeignKey(
        Vehiculo,
        on_delete=models.PROTECT,
        related_name="registros",
        verbose_name="vehículo",
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="registros",
        verbose_name="categoría",
    )
    fecha = models.DateField("fecha de la actividad")
    descripcion = models.TextField("descripción")
    # Decimal y no float, para que los totales sean exactos.
    costo = models.DecimalField("costo", max_digits=12, decimal_places=2)
    kilometraje = models.PositiveIntegerField("kilometraje")
    creado = models.DateTimeField("creado", auto_now_add=True)
    actualizado = models.DateTimeField("actualizado", auto_now=True)

    class Meta:
        verbose_name = "registro"
        verbose_name_plural = "registros"
        ordering = ["-fecha", "-id"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(costo__gte=0),
                name="registro_costo_no_negativo",
                violation_error_message="El costo no puede ser negativo.",
            ),
        ]
        indexes = [
            models.Index(fields=["vehiculo", "fecha"], name="registro_vehiculo_fecha_idx"),
        ]

    def __str__(self):
        return f"{self.fecha} · {self.categoria} · {self.vehiculo}"

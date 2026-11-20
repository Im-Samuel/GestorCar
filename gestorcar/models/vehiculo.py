import re

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

ANIO_MINIMO = 1900


def normalizar_placa(placa):
    """Deja la placa en mayúsculas y sin espacios ni guiones: "abc-123" -> "ABC123"."""
    return re.sub(r"[\s-]", "", placa or "").upper()


class Vehiculo(models.Model):
    class Tipo(models.TextChoices):
        AUTOMOVIL = "automovil", "Automóvil"
        CAMIONETA = "camioneta", "Camioneta"
        MOTOCICLETA = "motocicleta", "Motocicleta"
        CAMION = "camion", "Camión"
        OTRO = "otro", "Otro"

    class Estado(models.TextChoices):
        # El orden alfabético de los valores deja los activos antes que los retirados.
        ACTIVO = "activo", "Activo"
        RETIRADO = "retirado", "Retirado"

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="vehiculos",
        verbose_name="usuario",
    )
    marca = models.CharField("marca", max_length=80)
    modelo = models.CharField("modelo", max_length=80)
    anio = models.PositiveSmallIntegerField("año")
    placa = models.CharField("placa", max_length=15)
    kilometraje = models.PositiveIntegerField("kilometraje")
    tipo = models.CharField("tipo", max_length=20, choices=Tipo.choices)
    estado = models.CharField(
        "estado", max_length=10, choices=Estado.choices, default=Estado.ACTIVO
    )
    creado = models.DateTimeField("creado", auto_now_add=True)
    actualizado = models.DateTimeField("actualizado", auto_now=True)

    class Meta:
        verbose_name = "vehículo"
        verbose_name_plural = "vehículos"
        ordering = ["estado", "marca", "modelo"]
        constraints = [
            models.UniqueConstraint(
                fields=["usuario", "placa"],
                name="vehiculo_placa_unica_por_usuario",
                violation_error_message="Ya tienes un vehículo registrado con esta placa.",
            ),
            models.CheckConstraint(
                condition=models.Q(anio__gte=1900),
                name="vehiculo_anio_desde_1900",
                violation_error_message="El año debe ser 1900 o posterior.",
            ),
        ]

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.placa})"

    def save(self, *args, **kwargs):
        # bulk_create() y update() no pasan por aquí: quien los use debe normalizar antes.
        self.placa = normalizar_placa(self.placa)
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        self.placa = normalizar_placa(self.placa)
        # Reglas del año con el error en el campo (la base de datos también exige >= 1900).
        # Se validan aquí y no con validadores del campo para no generar una migración.
        if self.anio is not None:
            anio_maximo = timezone.localdate().year + 1
            if self.anio < ANIO_MINIMO:
                raise ValidationError({"anio": f"El año debe ser {ANIO_MINIMO} o posterior."})
            if self.anio > anio_maximo:
                raise ValidationError({"anio": f"El año no puede ser posterior a {anio_maximo}."})

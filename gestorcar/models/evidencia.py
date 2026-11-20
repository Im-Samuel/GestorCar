from django.db import models

from .registro import Registro


class Evidencia(models.Model):
    """Archivo que respalda un registro (factura, foto, cotización o comprobante)."""

    class Tipo(models.TextChoices):
        FACTURA = "factura", "Factura"
        FOTOGRAFIA = "fotografia", "Fotografía"
        COTIZACION = "cotizacion", "Cotización"
        COMPROBANTE = "comprobante", "Comprobante"

    registro = models.ForeignKey(
        Registro,
        on_delete=models.CASCADE,
        related_name="evidencias",
        verbose_name="registro",
    )
    # La validación de formato y tamaño, y dónde se guardan los archivos, es ISSUE-006.
    archivo = models.FileField("archivo", upload_to="evidencias/%Y/%m/")
    tipo = models.CharField("tipo", max_length=20, choices=Tipo.choices)
    nombre_original = models.CharField("nombre original", max_length=255, blank=True)
    subido = models.DateTimeField("subido", auto_now_add=True)

    class Meta:
        verbose_name = "evidencia"
        verbose_name_plural = "evidencias"
        ordering = ["subido"]

    def __str__(self):
        return self.nombre_original or self.archivo.name

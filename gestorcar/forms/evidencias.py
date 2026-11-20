"""Formulario de evidencias adjuntas a un registro (ISSUE-006)."""

from django import forms

from gestorcar.models import Evidencia

EXTENSIONES_PERMITIDAS = {".pdf", ".jpg", ".jpeg", ".png", ".webp"}
TAMANO_MAXIMO_MB = 10
TAMANO_MAXIMO_BYTES = TAMANO_MAXIMO_MB * 1024 * 1024


class EvidenciaForm(forms.ModelForm):
    class Meta:
        model = Evidencia
        fields = ("tipo", "archivo")
        help_texts = {
            "archivo": f"Formatos aceptados: PDF, JPG, PNG, WEBP. Máximo {TAMANO_MAXIMO_MB} MB.",
        }

    def clean_archivo(self):
        archivo = self.cleaned_data.get("archivo")
        if not archivo:
            return archivo

        nombre = archivo.name.lower()
        extension = "." + nombre.rsplit(".", 1)[-1] if "." in nombre else ""
        if extension not in EXTENSIONES_PERMITIDAS:
            raise forms.ValidationError(
                f"Formato no permitido. Use: {', '.join(sorted(EXTENSIONES_PERMITIDAS))}."
            )

        if archivo.size > TAMANO_MAXIMO_BYTES:
            raise forms.ValidationError(
                f"El archivo supera el límite de {TAMANO_MAXIMO_MB} MB."
            )

        return archivo

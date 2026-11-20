"""Formulario de importación masiva de registros (ISSUE-012)."""

from django import forms


class ImportarRegistrosForm(forms.Form):
    archivo = forms.FileField(
        label="Archivo CSV",
        help_text="Columnas requeridas: fecha (AAAA-MM-DD), categoria, descripcion, costo, kilometraje.",
    )

    def clean_archivo(self):
        archivo = self.cleaned_data.get("archivo")
        if archivo:
            nombre = archivo.name.lower()
            if not nombre.endswith(".csv"):
                raise forms.ValidationError("Solo se aceptan archivos .csv.")
        return archivo

"""Formulario de filtros para el historial de registros (ISSUE-008)."""

from django import forms

from gestorcar.models import Categoria


class HistorialFiltroForm(forms.Form):
    fecha_desde = forms.DateField(
        label="Desde",
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    fecha_hasta = forms.DateField(
        label="Hasta",
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    categoria = forms.ModelChoiceField(
        label="Categoría",
        queryset=Categoria.objects.order_by("tipo_actividad", "nombre"),
        required=False,
        empty_label="Todas las categorías",
    )
    tipo_actividad = forms.ChoiceField(
        label="Tipo de actividad",
        choices=[("", "Todos los tipos")] + Categoria.TipoActividad.choices,
        required=False,
    )

    def clean(self):
        datos = super().clean()
        desde = datos.get("fecha_desde")
        hasta = datos.get("fecha_hasta")
        if desde and hasta and desde > hasta:
            raise forms.ValidationError("La fecha de inicio no puede ser posterior a la fecha de fin.")
        return datos

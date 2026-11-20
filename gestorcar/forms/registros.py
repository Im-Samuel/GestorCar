"""Formulario de gastos e intervenciones (ISSUE-005)."""

from django import forms
from django.utils import timezone

from gestorcar.models import Categoria, Registro


class RegistroForm(forms.ModelForm):
    """Registro y edición de un gasto o intervención de un vehículo del usuario."""

    class Meta:
        model = Registro
        fields = ("fecha", "categoria", "descripcion", "costo", "kilometraje")
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date"}),
            "descripcion": forms.Textarea(attrs={"rows": 3}),
        }
        help_texts = {
            "costo": "Valor en pesos. No puede ser negativo.",
            "kilometraje": "Kilometraje del vehículo en el momento de la actividad.",
            "fecha": "Fecha en que se realizó la actividad.",
        }

    def __init__(self, *args, vehiculo, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.vehiculo = vehiculo
        # Ordenar categorías por tipo y luego nombre para facilitar la selección.
        self.fields["categoria"].queryset = Categoria.objects.order_by(
            "tipo_actividad", "nombre"
        )
        self.fields["categoria"].empty_label = "— Selecciona una categoría —"

    def clean_fecha(self):
        fecha = self.cleaned_data.get("fecha")
        if fecha and fecha > timezone.localdate():
            raise forms.ValidationError("La fecha no puede ser futura.")
        return fecha

    def clean_costo(self):
        costo = self.cleaned_data.get("costo")
        if costo is not None and costo < 0:
            raise forms.ValidationError("El costo no puede ser negativo.")
        return costo

    def clean_kilometraje(self):
        km = self.cleaned_data.get("kilometraje")
        if km is not None and km < 0:
            raise forms.ValidationError("El kilometraje no puede ser negativo.")
        return km

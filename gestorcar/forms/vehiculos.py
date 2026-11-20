from django import forms

from gestorcar.models import Vehiculo, normalizar_placa


class VehiculoForm(forms.ModelForm):
    """Registro y edición de un vehículo del usuario autenticado."""

    class Meta:
        model = Vehiculo
        fields = ("marca", "modelo", "anio", "placa", "kilometraje", "tipo")
        widgets = {
            "placa": forms.TextInput(attrs={"autocapitalize": "characters"}),
        }
        help_texts = {
            "placa": "Se guarda en mayúsculas y sin espacios ni guiones.",
            "kilometraje": "Kilometraje actual del vehículo.",
        }

    def __init__(self, *args, usuario, **kwargs):
        super().__init__(*args, **kwargs)
        # `usuario` no es un campo del formulario: se asigna antes de validar para que
        # el modelo y la comprobación de placa sepan de quién es el vehículo.
        self.instance.usuario = usuario

    def clean_placa(self):
        placa = normalizar_placa(self.cleaned_data["placa"])
        if not placa:
            raise forms.ValidationError("Este campo es obligatorio.", code="required")
        # Django omite la restricción única (usuario, placa) porque `usuario` no está en el
        # formulario; se comprueba aquí para mostrar el error junto al campo.
        repetida = Vehiculo.objects.filter(usuario=self.instance.usuario, placa=placa).exclude(
            pk=self.instance.pk
        )
        if repetida.exists():
            raise forms.ValidationError(
                "Ya tienes un vehículo registrado con esta placa.", code="unique"
            )
        return placa

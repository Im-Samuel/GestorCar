from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from gestorcar.models import Usuario


class RegistroForm(UserCreationForm):
    """Crea una cuenta con nombre, apellido, correo y contraseña."""

    class Meta:
        model = Usuario
        fields = ("first_name", "last_name", "email")
        widgets = {
            "first_name": forms.TextInput(attrs={"autocomplete": "given-name"}),
            "last_name": forms.TextInput(attrs={"autocomplete": "family-name"}),
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Django enfoca el campo de inicio de sesión (el correo, tercero del formulario);
        # al teclado le conviene empezar por el primero.
        self.fields["email"].widget.attrs.pop("autofocus", None)
        self.fields["first_name"].widget.attrs["autofocus"] = True

    def clean_email(self):
        # La base de datos también lo impide, pero aquí el error queda junto al campo.
        email = self.cleaned_data["email"].lower()
        if Usuario.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "Ya existe una cuenta con este correo electrónico.", code="unique"
            )
        return email

    def validate_password_for_user(self, user, password_field_name="password1"):
        # Django muestra por defecto el error de contraseña débil en la confirmación;
        # aquí se muestra junto al campo de la contraseña.
        super().validate_password_for_user(user, password_field_name=password_field_name)


class IniciarSesionForm(AuthenticationForm):
    """Inicio de sesión con correo y contraseña."""

    username = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={"autofocus": True, "autocomplete": "email"}),
    )

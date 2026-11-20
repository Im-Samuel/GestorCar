from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models.functions import Lower


class UsuarioManager(BaseUserManager):
    """Crea usuarios identificados por correo en lugar de nombre de usuario."""

    use_in_migrations = True

    def _crear_usuario(self, email, password, **campos):
        if not email:
            raise ValueError("El correo electrónico es obligatorio.")
        usuario = self.model(email=self.normalize_email(email).lower(), **campos)
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_user(self, email, password=None, **campos):
        campos.setdefault("is_staff", False)
        campos.setdefault("is_superuser", False)
        return self._crear_usuario(email, password, **campos)

    def create_superuser(self, email, password=None, **campos):
        campos.setdefault("is_staff", True)
        campos.setdefault("is_superuser", True)
        if campos["is_staff"] is not True or campos["is_superuser"] is not True:
            raise ValueError("Un superusuario debe tener is_staff e is_superuser activos.")
        return self._crear_usuario(email, password, **campos)

    def get_by_natural_key(self, email):
        # Permite iniciar sesión sin importar mayúsculas en el correo.
        return self.get(email__iexact=email)


class Usuario(AbstractUser):
    """Usuario de GestorCar. Se identifica por su correo, que es único."""

    username = None
    email = models.EmailField("correo electrónico", unique=True)
    first_name = models.CharField("nombre", max_length=150)
    last_name = models.CharField("apellido", max_length=150)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UsuarioManager()

    class Meta:
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"
        ordering = ["email"]
        constraints = [
            models.UniqueConstraint(
                Lower("email"),
                name="usuario_email_unico_sin_mayusculas",
                violation_error_message="Ya existe un usuario con este correo electrónico.",
            ),
        ]

    def __str__(self):
        return self.email

    def clean(self):
        super().clean()
        self.email = self.email.lower()

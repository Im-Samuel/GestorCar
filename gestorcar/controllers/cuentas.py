"""Registro, inicio y cierre de sesión."""

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_not_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView

from gestorcar.forms.cuentas import IniciarSesionForm, RegistroForm


@method_decorator(login_not_required, name="dispatch")
class RegistroView(CreateView):
    form_class = RegistroForm
    template_name = "cuentas/registro.html"
    success_url = reverse_lazy("inicio")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("inicio")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        respuesta = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, f"¡Bienvenido a GestorCar, {self.object.first_name}!")
        return respuesta


class IniciarSesionView(LoginView):
    # LoginView ya viene marcada como accesible sin sesión.
    template_name = "cuentas/iniciar_sesion.html"
    authentication_form = IniciarSesionForm
    redirect_authenticated_user = True


class CerrarSesionView(LogoutView):
    """Solo acepta POST (botón con token CSRF en la barra de navegación)."""

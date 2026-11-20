"""Registro, consulta, edición y retiro de los vehículos del usuario."""

from django.contrib import messages
from django.db import IntegrityError, transaction
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from gestorcar.controllers.mixins import PropietarioMixin
from gestorcar.forms.vehiculos import VehiculoForm
from gestorcar.models import Vehiculo

PLACA_REPETIDA = "Ya tienes un vehículo registrado con esta placa."


class VehiculoListaView(PropietarioMixin, ListView):
    # El orden del modelo (estado, marca, modelo) deja los activos primero.
    model = Vehiculo
    template_name = "vehiculos/lista.html"
    context_object_name = "vehiculos"


class VehiculoDetalleView(PropietarioMixin, DetailView):
    model = Vehiculo
    template_name = "vehiculos/detalle.html"
    context_object_name = "vehiculo"


class VehiculoFormularioMixin:
    """Comportamiento compartido por el registro y la edición."""

    model = Vehiculo
    form_class = VehiculoForm
    template_name = "vehiculos/formulario.html"
    mensaje_exito = ""

    def get_form_kwargs(self):
        return {**super().get_form_kwargs(), "usuario": self.request.user}

    def form_valid(self, form):
        try:
            # Punto de guardado propio: si dos peticiones registran la misma placa a la
            # vez, la base de datos rechaza la segunda sin romper la transacción.
            with transaction.atomic():
                self.object = form.save()
        except IntegrityError:
            form.add_error("placa", PLACA_REPETIDA)
            return self.form_invalid(form)
        messages.success(self.request, self.mensaje_exito)
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse("vehiculos:detalle", args=[self.object.pk])


class VehiculoCrearView(VehiculoFormularioMixin, CreateView):
    mensaje_exito = "Vehículo registrado."


class VehiculoEditarView(PropietarioMixin, VehiculoFormularioMixin, UpdateView):
    mensaje_exito = "Vehículo actualizado."


class VehiculoRetirarView(PropietarioMixin, DetailView):
    """GET muestra la confirmación; solo POST cambia el estado."""

    model = Vehiculo
    template_name = "vehiculos/confirmar_retiro.html"
    context_object_name = "vehiculo"

    def post(self, request, *args, **kwargs):
        vehiculo = self.get_object()
        if vehiculo.estado == Vehiculo.Estado.RETIRADO:
            messages.info(request, "Este vehículo ya estaba retirado.")
        else:
            vehiculo.estado = Vehiculo.Estado.RETIRADO
            vehiculo.save(update_fields=["estado", "actualizado"])
            messages.success(request, "Vehículo retirado. Su historial se conserva.")
        return redirect("vehiculos:detalle", pk=vehiculo.pk)

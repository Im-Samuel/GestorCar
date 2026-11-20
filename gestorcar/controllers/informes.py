"""Vistas de informes y comparación de vehículos (ISSUE-010, ISSUE-011)."""

from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from gestorcar.models import Vehiculo
from gestorcar.services.totales import (
    total_por_categoria,
    total_por_mes,
    total_por_tipo_actividad,
    total_vehiculo,
    totales_por_vehiculo,
)


class InformeVehiculoView(TemplateView):
    """
    Resumen de inversión por categoría, tipo de actividad y evolución mensual
    para un vehículo del usuario (RF-16, RF-17).
    """

    template_name = "vehiculos/informes.html"

    def get_object(self):
        if not hasattr(self, "_vehiculo"):
            self._vehiculo = get_object_or_404(
                Vehiculo, pk=self.kwargs["pk"], usuario=self.request.user
            )
        return self._vehiculo

    def get(self, request, *args, **kwargs):
        self.get_object()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        vehiculo = self.get_object()
        return super().get_context_data(
            **kwargs,
            vehiculo=vehiculo,
            total=total_vehiculo(vehiculo),
            por_categoria=total_por_categoria(vehiculo),
            por_tipo=total_por_tipo_actividad(vehiculo),
            por_mes=total_por_mes(vehiculo),
        )


class ComparacionVehiculosView(TemplateView):
    """
    Tabla comparativa de todos los vehículos del usuario: total invertido,
    desglose por tipo de actividad y gastos de mantenimiento (RF-18).
    """

    template_name = "vehiculos/comparar.html"

    def get_context_data(self, **kwargs):
        vehiculos = list(
            Vehiculo.objects.filter(usuario=self.request.user)
        )
        filas = totales_por_vehiculo(vehiculos)
        for fila in filas:
            fila["por_tipo"] = {
                r["tipo_actividad"]: r["total"]
                for r in total_por_tipo_actividad(fila["vehiculo"])
            }
        return super().get_context_data(**kwargs, filas=filas, vehiculos=vehiculos)

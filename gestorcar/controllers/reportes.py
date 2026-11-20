"""Vista de reporte mensual consolidado (ISSUE-013, RF-21)."""

import datetime

from django import forms
from django.db.models import F, Sum
from django.views.generic import TemplateView

from gestorcar.models import Registro, Vehiculo


class _MesForm(forms.Form):
    anio = forms.IntegerField(
        label="Año",
        min_value=1900,
        widget=forms.NumberInput(attrs={"min": "1900"}),
    )
    mes = forms.IntegerField(
        label="Mes",
        min_value=1,
        max_value=12,
        widget=forms.NumberInput(attrs={"min": "1", "max": "12"}),
    )
    vehiculo = forms.IntegerField(
        label="Vehículo",
        required=False,
    )


class ReporteMensualView(TemplateView):
    """
    Reporte mensual de un vehículo o de todos los del usuario.
    Selector de mes + alcance; muestra total y desglose por categoría (RF-21).
    """

    template_name = "reportes/mensual.html"

    def _rango_mes(self, anio: int, mes: int):
        primer = datetime.date(anio, mes, 1)
        if mes == 12:
            ultimo = datetime.date(anio + 1, 1, 1) - datetime.timedelta(days=1)
        else:
            ultimo = datetime.date(anio, mes + 1, 1) - datetime.timedelta(days=1)
        return primer, ultimo

    def get_context_data(self, **kwargs):
        hoy = datetime.date.today()
        datos_form = self.request.GET or {"anio": hoy.year, "mes": hoy.month}
        form = _MesForm(datos_form)

        reporte = None
        if form.is_valid():
            anio = form.cleaned_data["anio"]
            mes = form.cleaned_data["mes"]
            vid = form.cleaned_data.get("vehiculo")
            primer, ultimo = self._rango_mes(anio, mes)

            vehiculos_usuario = list(Vehiculo.objects.filter(usuario=self.request.user))
            vehiculos_sel = [v for v in vehiculos_usuario if v.pk == vid] if vid else vehiculos_usuario

            filas = []
            total_global = 0
            for v in vehiculos_sel:
                qs = Registro.objects.filter(vehiculo=v, fecha__gte=primer, fecha__lte=ultimo)
                total_v = qs.aggregate(t=Sum("costo"))["t"] or 0
                por_cat = list(
                    qs.values(
                        nombre=F("categoria__nombre"),
                        tipo_actividad=F("categoria__tipo_actividad"),
                    )
                    .annotate(total=Sum("costo"))
                    .order_by("-total")
                )
                filas.append({"vehiculo": v, "total": total_v, "por_categoria": por_cat})
                total_global += total_v

            reporte = {
                "anio": anio,
                "mes": mes,
                "primer_dia": primer,
                "ultimo_dia": ultimo,
                "filas": filas,
                "total_global": total_global,
            }

        return super().get_context_data(
            **kwargs,
            form=form,
            reporte=reporte,
            vehiculos=Vehiculo.objects.filter(usuario=self.request.user),
        )

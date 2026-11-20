"""Registro, consulta, edición, eliminación e importación de gastos (ISSUE-005, ISSUE-007, ISSUE-012)."""

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView, View

from gestorcar.forms.evidencias import EvidenciaForm
from gestorcar.forms.historial import HistorialFiltroForm
from gestorcar.forms.importar import ImportarRegistrosForm
from gestorcar.forms.registros import RegistroForm
from gestorcar.models import Registro, Vehiculo
from gestorcar.services.importar import importar_desde_csv


class RegistroPorVehiculoMixin:
    """Resuelve el vehículo del usuario desde la URL y lo inyecta en el formulario."""

    campo_propietario = "vehiculo__usuario"

    def _vehiculo(self):
        if not hasattr(self, "_vehiculo_cache"):
            self._vehiculo_cache = get_object_or_404(
                Vehiculo, pk=self.kwargs["vehiculo_pk"], usuario=self.request.user
            )
        return self._vehiculo_cache

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs, vehiculo=self._vehiculo())

    def get_form_kwargs(self):
        return {**super().get_form_kwargs(), "vehiculo": self._vehiculo()}

    def get_queryset(self):
        return Registro.objects.filter(vehiculo=self._vehiculo()).select_related("categoria")


class RegistroListaView(RegistroPorVehiculoMixin, ListView):
    model = Registro
    template_name = "registros/lista.html"
    context_object_name = "registros"

    def get_queryset(self):
        qs = super().get_queryset()
        form = HistorialFiltroForm(self.request.GET or None)
        if form.is_valid():
            if form.cleaned_data.get("fecha_desde"):
                qs = qs.filter(fecha__gte=form.cleaned_data["fecha_desde"])
            if form.cleaned_data.get("fecha_hasta"):
                qs = qs.filter(fecha__lte=form.cleaned_data["fecha_hasta"])
            if form.cleaned_data.get("categoria"):
                qs = qs.filter(categoria=form.cleaned_data["categoria"])
            if form.cleaned_data.get("tipo_actividad"):
                qs = qs.filter(categoria__tipo_actividad=form.cleaned_data["tipo_actividad"])
        return qs

    def get_context_data(self, **kwargs):
        filtro_form = HistorialFiltroForm(self.request.GET or None)
        qs = self.get_queryset()
        from django.db.models import Sum
        total = qs.aggregate(total=Sum("costo"))["total"]
        return super().get_context_data(**kwargs, filtro_form=filtro_form, total=total)


class RegistroDetalleView(RegistroPorVehiculoMixin, DetailView):
    model = Registro
    template_name = "registros/detalle.html"
    context_object_name = "registro"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs, evidencia_form=EvidenciaForm())


class RegistroFormularioMixin(RegistroPorVehiculoMixin):
    model = Registro
    form_class = RegistroForm
    template_name = "registros/formulario.html"
    mensaje_exito = ""

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, self.mensaje_exito)
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse(
            "registros:detalle",
            kwargs={"vehiculo_pk": self._vehiculo().pk, "pk": self.object.pk},
        )


class RegistroCrearView(RegistroFormularioMixin, CreateView):
    mensaje_exito = "Registro guardado."


class RegistroEditarView(RegistroFormularioMixin, UpdateView):
    mensaje_exito = "Registro actualizado."


class RegistroEliminarView(View):
    """GET muestra la confirmación; POST elimina el registro."""

    def _registro(self):
        return get_object_or_404(
            Registro,
            pk=self.kwargs["pk"],
            vehiculo__pk=self.kwargs["vehiculo_pk"],
            vehiculo__usuario=self.request.user,
        )

    def get(self, request, *args, **kwargs):
        registro = self._registro()
        return render(
            request,
            "registros/confirmar_eliminacion.html",
            {"registro": registro, "vehiculo": registro.vehiculo},
        )

    def post(self, request, *args, **kwargs):
        registro = self._registro()
        vehiculo_pk = registro.vehiculo.pk
        registro.delete()
        messages.success(request, "Registro eliminado.")
        return redirect("registros:lista", vehiculo_pk=vehiculo_pk)


class RegistroImportarView(View):
    """Carga masiva de registros desde un archivo CSV (ISSUE-012, RF-20)."""

    def _vehiculo(self):
        return get_object_or_404(
            Vehiculo, pk=self.kwargs["vehiculo_pk"], usuario=self.request.user
        )

    def get(self, request, *args, **kwargs):
        vehiculo = self._vehiculo()
        return render(request, "registros/importar.html", {
            "form": ImportarRegistrosForm(),
            "vehiculo": vehiculo,
        })

    def post(self, request, *args, **kwargs):
        vehiculo = self._vehiculo()
        form = ImportarRegistrosForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, "registros/importar.html", {"form": form, "vehiculo": vehiculo})

        resultado = importar_desde_csv(vehiculo, request.FILES["archivo"])
        return render(request, "registros/importar.html", {
            "form": ImportarRegistrosForm(),
            "vehiculo": vehiculo,
            "resultado": resultado,
        })

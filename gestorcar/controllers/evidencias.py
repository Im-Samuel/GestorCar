"""Subida, consulta y eliminación de evidencias de un registro (ISSUE-006)."""

import mimetypes
import os

from django.contrib import messages
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, View

from gestorcar.forms.evidencias import EvidenciaForm
from gestorcar.models import Evidencia, Registro

# Tipos MIME que el navegador puede mostrar como contenido activo.
# Para el resto se fuerza descarga con Content-Disposition: attachment.
MIME_INLINE = {"application/pdf", "image/jpeg", "image/png", "image/webp"}


def _registro_del_usuario(vehiculo_pk, registro_pk, usuario):
    return get_object_or_404(
        Registro,
        pk=registro_pk,
        vehiculo__pk=vehiculo_pk,
        vehiculo__usuario=usuario,
    )


class EvidenciaCrearView(CreateView):
    """POST sube una evidencia al registro; redirige de vuelta al detalle."""

    model = Evidencia
    form_class = EvidenciaForm
    # No tiene plantilla propia: el formulario se incrusta en registros/detalle.html.
    template_name = "registros/detalle.html"

    def _registro(self):
        if not hasattr(self, "_registro_cache"):
            self._registro_cache = _registro_del_usuario(
                self.kwargs["vehiculo_pk"],
                self.kwargs["registro_pk"],
                self.request.user,
            )
        return self._registro_cache

    def get_context_data(self, **kwargs):
        registro = self._registro()
        return super().get_context_data(
            **kwargs,
            registro=registro,
            vehiculo=registro.vehiculo,
        )

    def form_valid(self, form):
        archivo = form.cleaned_data["archivo"]
        form.instance.registro = self._registro()
        form.instance.nombre_original = os.path.basename(archivo.name)
        form.save()
        messages.success(self.request, "Evidencia adjuntada.")
        return redirect(
            "registros:detalle",
            vehiculo_pk=self.kwargs["vehiculo_pk"],
            pk=self.kwargs["registro_pk"],
        )

    def form_invalid(self, form):
        messages.error(
            self.request,
            "No se pudo subir el archivo: "
            + " ".join(e for errors in form.errors.values() for e in errors),
        )
        return redirect(
            "registros:detalle",
            vehiculo_pk=self.kwargs["vehiculo_pk"],
            pk=self.kwargs["registro_pk"],
        )


class EvidenciaDescargarView(View):
    """Descarga o muestra una evidencia verificando que sea del usuario."""

    def get(self, request, vehiculo_pk, registro_pk, pk):
        registro = _registro_del_usuario(vehiculo_pk, registro_pk, request.user)
        evidencia = get_object_or_404(Evidencia, pk=pk, registro=registro)

        if not evidencia.archivo.storage.exists(evidencia.archivo.name):
            raise Http404

        mime, _ = mimetypes.guess_type(evidencia.archivo.name)
        as_attachment = mime not in MIME_INLINE if mime else True

        return FileResponse(
            evidencia.archivo.open("rb"),
            as_attachment=as_attachment,
            filename=evidencia.nombre_original or os.path.basename(evidencia.archivo.name),
            content_type=mime or "application/octet-stream",
        )


class EvidenciaEliminarView(View):
    """POST elimina una evidencia verificando que pertenezca al usuario."""

    def post(self, request, vehiculo_pk, registro_pk, pk):
        registro = _registro_del_usuario(vehiculo_pk, registro_pk, request.user)
        evidencia = get_object_or_404(Evidencia, pk=pk, registro=registro)
        evidencia.archivo.delete(save=False)
        evidencia.delete()
        messages.success(request, "Evidencia eliminada.")
        return redirect("registros:detalle", vehiculo_pk=vehiculo_pk, pk=registro_pk)

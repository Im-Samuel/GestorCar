"""Exportación del historial completo del usuario como JSON (ISSUE-017, RF-22)."""

import json
from datetime import datetime

from gestorcar.models import Vehiculo


def exportar_datos_usuario(usuario) -> str:
    """
    Serializa todos los vehículos y registros del usuario.
    Devuelve una cadena JSON con indentación, lista para descarga.
    """
    vehiculos = []
    for v in Vehiculo.objects.filter(usuario=usuario).prefetch_related(
        "registros__categoria"
    ):
        registros = []
        for r in v.registros.all():
            registros.append(
                {
                    "fecha": str(r.fecha),
                    "categoria": r.categoria.nombre,
                    "tipo_actividad": r.categoria.tipo_actividad,
                    "descripcion": r.descripcion,
                    "costo": str(r.costo),
                    "kilometraje": r.kilometraje,
                }
            )
        vehiculos.append(
            {
                "marca": v.marca,
                "modelo": v.modelo,
                "anio": v.anio,
                "placa": v.placa,
                "tipo": v.tipo,
                "estado": v.estado,
                "kilometraje": v.kilometraje,
                "registros": registros,
            }
        )

    return json.dumps(
        {
            "version": "1",
            "exportado_en": datetime.now().isoformat(timespec="seconds"),
            "total_vehiculos": len(vehiculos),
            "vehiculos": vehiculos,
        },
        ensure_ascii=False,
        indent=2,
    )

"""
Cálculo centralizado de totales y agregaciones (ISSUE-009, RF-19).

Todas las funciones reciben un queryset de Registro (o un vehículo/usuario)
y devuelven valores Decimal exactos. No dependen de la interfaz web: se pueden
llamar desde vistas, tareas, scripts o tests sin importar nada de Django views.
"""

from decimal import Decimal

from django.db.models import DecimalField, ExpressionWrapper, F, QuerySet, Sum
from django.db.models.functions import TruncMonth, TruncYear

from gestorcar.models import Registro


def _qs_vehiculo(vehiculo) -> QuerySet:
    return Registro.objects.filter(vehiculo=vehiculo)


# ── Total general ─────────────────────────────────────────────────────────────

def total_vehiculo(vehiculo) -> Decimal:
    """Suma todos los costos de un vehículo."""
    resultado = _qs_vehiculo(vehiculo).aggregate(total=Sum("costo"))
    return resultado["total"] or Decimal("0")


def total_qs(qs: QuerySet) -> Decimal:
    """Suma los costos de un queryset de Registro arbitrario."""
    resultado = qs.aggregate(total=Sum("costo"))
    return resultado["total"] or Decimal("0")


# ── Subtotales por categoría ──────────────────────────────────────────────────

def total_por_categoria(vehiculo) -> list[dict]:
    """
    Devuelve lista de dicts {categoria_id, nombre, tipo_actividad, total}
    ordenada de mayor a menor costo.
    """
    return list(
        _qs_vehiculo(vehiculo)
        .values(
            cat_id=F("categoria__id"),
            nombre=F("categoria__nombre"),
            tipo_actividad=F("categoria__tipo_actividad"),
        )
        .annotate(total=Sum("costo"))
        .order_by("-total")
    )


def total_por_tipo_actividad(vehiculo) -> list[dict]:
    """
    Devuelve lista de dicts {tipo_actividad, total} ordenada de mayor a menor.
    """
    return list(
        _qs_vehiculo(vehiculo)
        .values(tipo_actividad=F("categoria__tipo_actividad"))
        .annotate(total=Sum("costo"))
        .order_by("-total")
    )


# ── Subtotales por período ────────────────────────────────────────────────────

def total_por_mes(vehiculo) -> list[dict]:
    """
    Devuelve lista de dicts {mes (date), total} ordenada cronológicamente.
    `mes` es el primer día del mes (año-mes-01).
    """
    return list(
        _qs_vehiculo(vehiculo)
        .annotate(mes=TruncMonth("fecha"))
        .values("mes")
        .annotate(total=Sum("costo"))
        .order_by("mes")
    )


def total_por_anio(vehiculo) -> list[dict]:
    """
    Devuelve lista de dicts {anio (date), total} ordenada cronológicamente.
    """
    return list(
        _qs_vehiculo(vehiculo)
        .annotate(anio=TruncYear("fecha"))
        .values("anio")
        .annotate(total=Sum("costo"))
        .order_by("anio")
    )


# ── Rango de fechas ───────────────────────────────────────────────────────────

def total_en_rango(vehiculo, fecha_desde, fecha_hasta) -> Decimal:
    """Suma los costos de un vehículo entre dos fechas (inclusive)."""
    resultado = (
        _qs_vehiculo(vehiculo)
        .filter(fecha__gte=fecha_desde, fecha__lte=fecha_hasta)
        .aggregate(total=Sum("costo"))
    )
    return resultado["total"] or Decimal("0")


# ── Comparación entre vehículos ───────────────────────────────────────────────

def totales_por_vehiculo(vehiculos) -> list[dict]:
    """
    Recibe un iterable de vehículos y devuelve lista de dicts
    {vehiculo, total} ordenada de mayor a menor gasto.
    Útil para comparar vehículos del mismo usuario (ISSUE-011).
    """
    return sorted(
        [{"vehiculo": v, "total": total_vehiculo(v)} for v in vehiculos],
        key=lambda d: d["total"],
        reverse=True,
    )

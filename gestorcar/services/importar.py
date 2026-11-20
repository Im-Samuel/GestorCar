"""Servicio de importación masiva de registros desde CSV (ISSUE-012, RF-20)."""

import csv
import datetime
import io
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation

from gestorcar.models import Categoria, Registro


CABECERAS_REQUERIDAS = {"fecha", "categoria", "descripcion", "costo", "kilometraje"}


@dataclass
class FilaResultado:
    numero: int
    datos: dict
    error: str = ""

    @property
    def aceptada(self) -> bool:
        return not self.error


@dataclass
class ResultadoImportacion:
    aceptadas: list[FilaResultado] = field(default_factory=list)
    rechazadas: list[FilaResultado] = field(default_factory=list)

    @property
    def total(self) -> int:
        return len(self.aceptadas) + len(self.rechazadas)


def _validar_fila(numero: int, fila: dict, catalogo: dict[str, Categoria]) -> FilaResultado:
    datos = {k: v.strip() for k, v in fila.items()}
    resultado = FilaResultado(numero=numero, datos=datos)

    # fecha
    try:
        fecha = datetime.date.fromisoformat(datos.get("fecha", ""))
    except ValueError:
        resultado.error = "fecha inválida (use AAAA-MM-DD)"
        return resultado
    if fecha > datetime.date.today():
        resultado.error = "la fecha no puede ser futura"
        return resultado

    # categoria
    nombre_cat = datos.get("categoria", "")
    if nombre_cat not in catalogo:
        resultado.error = f"categoría '{nombre_cat}' no existe en el catálogo"
        return resultado

    # descripcion
    if not datos.get("descripcion"):
        resultado.error = "la descripción es obligatoria"
        return resultado

    # costo
    try:
        costo = Decimal(datos.get("costo", ""))
        if costo < 0:
            raise ValueError
    except (InvalidOperation, ValueError):
        resultado.error = "costo inválido (debe ser un número >= 0)"
        return resultado

    # kilometraje
    try:
        km = int(datos.get("kilometraje", ""))
        if km < 0:
            raise ValueError
    except (ValueError, TypeError):
        resultado.error = "kilometraje inválido (debe ser un entero >= 0)"
        return resultado

    resultado.datos = {
        "fecha": fecha,
        "categoria": catalogo[nombre_cat],
        "descripcion": datos["descripcion"],
        "costo": costo,
        "kilometraje": km,
    }
    return resultado


def importar_desde_csv(vehiculo, archivo_binario) -> ResultadoImportacion:
    """
    Lee un archivo CSV y devuelve un ResultadoImportacion con filas aceptadas y
    rechazadas. Las filas aceptadas se guardan en la base de datos en un solo
    bulk_create.
    """
    resultado = ResultadoImportacion()

    try:
        texto = archivo_binario.read().decode("utf-8-sig")
    except UnicodeDecodeError:
        resultado.rechazadas.append(
            FilaResultado(numero=0, datos={}, error="el archivo no es UTF-8 válido")
        )
        return resultado

    reader = csv.DictReader(io.StringIO(texto))

    if not reader.fieldnames:
        resultado.rechazadas.append(
            FilaResultado(numero=0, datos={}, error="el archivo está vacío o no tiene cabeceras")
        )
        return resultado

    cabeceras = {c.strip().lower() for c in reader.fieldnames}
    faltantes = CABECERAS_REQUERIDAS - cabeceras
    if faltantes:
        resultado.rechazadas.append(
            FilaResultado(
                numero=0,
                datos={},
                error=f"faltan columnas: {', '.join(sorted(faltantes))}",
            )
        )
        return resultado

    catalogo = {c.nombre: c for c in Categoria.objects.all()}

    for i, fila in enumerate(reader, start=1):
        fila_normalizada = {k.strip().lower(): v for k, v in fila.items()}
        fila_resultado = _validar_fila(i, fila_normalizada, catalogo)
        if fila_resultado.aceptada:
            resultado.aceptadas.append(fila_resultado)
        else:
            resultado.rechazadas.append(fila_resultado)

    if resultado.aceptadas:
        Registro.objects.bulk_create([
            Registro(vehiculo=vehiculo, **f.datos)
            for f in resultado.aceptadas
        ])

    return resultado

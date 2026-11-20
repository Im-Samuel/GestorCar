# Design

## Context

El proyecto no tiene apps propias ni migraciones aplicadas que conservar. Este
cambio parte del entorno de ISSUE-000 (PostgreSQL, configuración por variables
de entorno, `pytest-django`). Ver `proposal.md` (Why) para la motivación y la
validación de la propuesta del equipo, y `specs/integridad-datos/spec.md` para
las reglas exigidas.

## Goals / Non-Goals

**Goals:**
- Un modelo de datos completo y estable para los Sprints 1 a 3.
- Que las reglas de integridad las aplique la base de datos y no solo los
  formularios, para que también protejan la importación (ISSUE-012) y el admin.

**Non-Goals:**
- Validaciones con mensajes para el usuario (ISSUE-003 y ISSUE-005).
- Validación de formato y tamaño de archivos y configuración de `MEDIA_ROOT`
  (ISSUE-006).
- Carga del catálogo de categorías (ISSUE-004).
- Totales almacenados: se calculan con consultas (ISSUE-009).

## Decisions

### 1. Modelo de datos

```
Usuario 1──* Vehiculo 1──* Registro *──1 Categoria
                              │
                              1──* Evidencia
```

| Modelo | Archivo en `gestorcar/models/` | Campos |
|---|---|---|
| `Usuario` | `usuario.py` | `id`, `email` (único), `first_name`, `last_name`, `password` (hash), `is_active`, `is_staff`, `date_joined` |
| `Vehiculo` | `vehiculo.py` | `usuario` → Usuario, `marca`, `modelo`, `anio`, `placa`, `kilometraje`, `tipo`, `estado`, `creado`, `actualizado` |
| `Categoria` | `categoria.py` | `nombre` (único), `tipo_actividad` |
| `Registro` | `registro.py` | `vehiculo` → Vehiculo, `categoria` → Categoria, `fecha`, `descripcion`, `costo`, `kilometraje`, `creado`, `actualizado` |
| `Evidencia` | `evidencia.py` | `registro` → Registro, `archivo`, `tipo`, `nombre_original`, `subido` |

Opciones fijas (`TextChoices`):
- `Vehiculo.tipo`: automóvil, camioneta, motocicleta, camión, otro.
- `Vehiculo.estado`: activo (por defecto), retirado.
- `Categoria.tipo_actividad`: mantenimiento, reparación, modificación, otro.
- `Evidencia.tipo`: factura, fotografía, cotización, comprobante.

Correspondencia con la propuesta del equipo: el `I.D.` es la clave primaria
automática; `Nombre`, `Apellido`, `correo` y `Password` pasan a `first_name`,
`last_name`, `email` y `password`; `Tipo de gasto` pasa a ser la relación con
`Categoria`; `fotos` pasa a `archivo` con un `tipo`, porque RF-10 también exige
facturas, cotizaciones y comprobantes.

- **Alternativa descartada — entidad `Gasto` separada de `Registro`:**
  duplicaría fecha, costo y kilometraje, y obligaría a mantener sincronizados
  dos registros por cada actividad. Gasto e intervención se distinguen por la
  categoría.
- **Alternativa descartada — guardar `edad`:** ningún requisito la usa y
  cambia sola con el tiempo. Si en el futuro hiciera falta, se guardaría la
  fecha de nacimiento.

### 2. Usuario propio basado en `AbstractUser`, sin `username`
`Usuario` hereda de `AbstractUser`, elimina `username`, usa
`USERNAME_FIELD = "email"` y un `UsuarioManager` propio con `create_user` y
`create_superuser` que normalizan el correo a minúsculas. La unicidad sin
distinguir mayúsculas se garantiza con un `UniqueConstraint` sobre
`Lower("email")`.
- **Por qué ahora:** Django exige definir `AUTH_USER_MODEL` antes de la
  primera migración.
- **Alternativa:** el `User` de Django con un perfil aparte; obliga a iniciar
  sesión con nombre de usuario, contrario a HU-01.

### 3. Una sola app organizada por capas MVC
El equipo eligió una estructura por capas que refleja el MVC del backlog. Como
Django exige que los modelos pertenezcan a una app registrada, todo vive en una
única app, `gestorcar`, dividida por capas:

```
gestorcar/
├── models/        M: un archivo por entidad; __init__.py los expone todos
├── controllers/   C: lo que Django llama "views"
├── views/         V: plantillas HTML
├── forms/         validación de formularios
├── urls/          rutas por área (cuentas, vehiculos)
├── admin/         un módulo por entidad
├── migrations/    un único historial de migraciones
└── tests/         un archivo de pruebas por entidad o área
```

La carpeta de plantillas se llama `views/` por el MVC y se declara en
`TEMPLATES["DIRS"]`, porque Django solo busca automáticamente en
`<app>/templates/`.
- **Alternativa descartada: una app por dominio** (`cuentas`, `vehiculos`,
  `registros`), que es la convención de Django y reparte las migraciones en
  historiales independientes. El equipo prefirió la separación por capas.
- **Alternativa descartada: carpetas `models/` y `controllers/` en la raíz
  del proyecto.** Obligaría a registrar como app una carpeta llamada
  `models`, que choca con la forma en que Django y el equipo nombran los
  imports.

### 4. Integridad en la base de datos
- `on_delete=PROTECT` en `Vehiculo.usuario`, `Registro.vehiculo` y
  `Registro.categoria` (historial protegido, RNF-09).
- `on_delete=CASCADE` en `Evidencia.registro` (una evidencia no tiene sentido
  sin su registro; RF-11 permite eliminar registros).
- `PositiveIntegerField` para kilometrajes (Django crea la restricción `>= 0`
  en PostgreSQL), `CheckConstraint` para `costo >= 0` y `anio >= 1900`.
- `costo` como `DecimalField(max_digits=12, decimal_places=2)`, nunca `float`,
  para que los totales sean exactos (RNF-06).
- `UniqueConstraint` en (`usuario`, `placa`) y en `Categoria.nombre`.
- Índice en (`vehiculo`, `fecha`) de `Registro` para el historial cronológico.

### 5. Placa normalizada al guardar
`Vehiculo.save()` y `Vehiculo.clean()` normalizan la placa: mayúsculas, sin
espacios ni guiones. Así la restricción única compara valores normalizados.
- **Riesgo aceptado:** `bulk_create` y `update()` no llaman a `save()`. La
  importación (ISSUE-012) debe normalizar antes de guardar.

### 6. Transacciones por petición
Se activa `ATOMIC_REQUESTS = True` en la configuración de la base de datos:
cada petición web se confirma completa o se revierte (RNF-08). Los procesos
fuera de una petición usan `transaction.atomic()` explícito.

### 7. Admin y pruebas
Los cinco modelos se registran en el admin con listados y filtros básicos,
útiles para que el equipo cargue datos antes de que existan las vistas. Las
pruebas de `pytest` validan cada escenario de la especificación contra
PostgreSQL.

## Risks / Trade-offs

- [Con una sola app, dos ramas que cambian modelos a la vez crean migraciones
  con el mismo número y Django rechaza aplicarlas] → Este cambio genera una
  única migración inicial; antes de tocar un modelo se avisa al equipo, y si
  aun así hay dos migraciones paralelas se resuelve con
  `python manage.py makemigrations --merge` o regenerando la más reciente.
- [La lista de tipos de vehículo o de evidencia resulta incompleta] → Agregar
  una opción no cambia el esquema de la base de datos; se ajusta sin
  migraciones complejas.
- [`PROTECT` impide borrar usuarios con datos desde el admin] → Aceptado: no
  hay requisito de borrar cuentas y RNF-09 prioriza conservar el historial.

## Migration Plan

1. Aplicar después de `configurar-entorno-desarrollo`.
2. Si alguien ejecutó `migrate` antes con el usuario por defecto de Django,
   debe borrar su volumen de base de datos (`docker compose down -v`) y migrar
   de nuevo; aún no hay datos reales.
3. **Reversión:** revertir el commit y recrear la base de datos.

## Open Questions

- Lista final de tipos de vehículo; se puede ampliar sin cambiar la
  especificación.

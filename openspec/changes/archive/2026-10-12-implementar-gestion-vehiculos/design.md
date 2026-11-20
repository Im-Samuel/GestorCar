# Design

## Context

`disenar-modelos-datos` deja `Vehiculo` con placa normalizada, restricción
única (`usuario`, `placa`), `anio >= 1900` y estados activo/retirado.
`implementar-autenticacion` deja la sesión obligatoria por defecto,
`PropietarioMixin`, `gestorcar/views/base.html` e `includes/campo.html`. Ver
`proposal.md` y `specs/gestion-vehiculos/spec.md`.

## Goals / Non-Goals

**Goals:**
- Un CRUD de vehículos que sirva de patrón para las vistas de gastos
  (ISSUE-005) y evidencias (ISSUE-006).

**Non-Goals:**
- Historial, totales o gráficos en el detalle del vehículo (ISSUE-008 a 010).
- Paginación del listado: un usuario tiene pocos vehículos.
- Reactivar o eliminar vehículos.

## Decisions

### 1. Vistas genéricas basadas en clases
`ListView`, `DetailView`, `CreateView` y `UpdateView` con `PropietarioMixin`
(`campo_propietario = "usuario"`), y una vista de retiro propia: `GET` muestra
la confirmación y `POST` cambia el estado.

| URL | Nombre | Vista |
|---|---|---|
| `/vehiculos/` | `vehiculos:lista` | listado |
| `/vehiculos/nuevo/` | `vehiculos:crear` | registro |
| `/vehiculos/<id>/` | `vehiculos:detalle` | detalle |
| `/vehiculos/<id>/editar/` | `vehiculos:editar` | edición |
| `/vehiculos/<id>/retirar/` | `vehiculos:retirar` | confirmación y retiro |

`/` redirige a `vehiculos:lista`, reemplazando la página de inicio
provisional.
- **Alternativa:** vistas basadas en funciones; más explícitas para aprender,
  pero repiten el filtrado por usuario que el mixin ya resuelve.

### 2. Validación en dos niveles
- **Modelo:** `Vehiculo.clean()` rechaza un año anterior a 1900 o mayor que el
  año actual más uno (RNF-07), con el error asociado al campo año y en español.
  La restricción `>= 1900` sigue además en la base de datos. Se usa `clean()` y
  no validadores del campo porque estos obligarían a crear una migración nueva
  (sin cambios en la base de datos) en el historial único que comparte el
  equipo. Como el error queda en el campo, Django no repite el mensaje de la
  restricción de la base de datos.
- **Formulario:** `VehiculoForm` (`ModelForm` con marca, modelo, año, placa,
  kilometraje y tipo) normaliza la placa en `clean_placa()` y comprueba que
  no exista otra igual del mismo usuario, excluyendo el propio vehículo al
  editar.
- **Por qué la comprobación manual de la placa:** `usuario` no es un campo del
  formulario, así que Django omite la restricción única al validar y el error
  llegaría como `IntegrityError` en lugar de un mensaje junto al campo. La
  vista asigna `form.instance.usuario = request.user` antes de validar.

### 3. Retiro lógico por `POST`
`retirar` solo cambia el estado con `POST` y token CSRF; un `GET` nunca
modifica datos. La pantalla de confirmación indica que el historial se
conserva. Repetir el retiro de un vehículo ya retirado no tiene efecto.

### 4. Orden del listado
`order_by("estado", "marca", "modelo")` con los valores de `TextChoices`
definidos para que "activo" quede antes que "retirado".

### 5. Pantallas (frontend)
Controladores en `gestorcar/controllers/vehiculos.py`, formulario en
`gestorcar/forms/vehiculos.py` y rutas en `gestorcar/urls/vehiculos.py`
(espacio de nombres `vehiculos`). Plantillas en `gestorcar/views/vehiculos/`,
todas heredan de `base.html`:
- `lista.html`: tabla en pantallas grandes y tarjetas apiladas en teléfono;
  insignia "Retirado" y estado vacío con botón "Registrar vehículo".
- `formulario.html`: compartida por registro y edición, con
  `includes/campo.html`.
- `detalle.html`: datos del vehículo y acciones "Editar" y "Retirar".
- `confirmar_retiro.html`: confirmación con botones "Retirar" y "Cancelar".

Los mensajes de éxito usan `django.contrib.messages`.

## Risks / Trade-offs

- [Dos peticiones simultáneas registran la misma placa] → La restricción de la
  base de datos rechaza la segunda; se captura `IntegrityError` en la vista y
  se muestra como error del campo.
- [El usuario reduce el kilometraje por error] → Se permite para poder
  corregir errores de digitación; la coherencia con los registros de gastos se
  valida en ISSUE-005.

## Migration Plan

Sin migraciones de base de datos. Reversión: revertir el commit; `/` vuelve a
la página de inicio provisional.

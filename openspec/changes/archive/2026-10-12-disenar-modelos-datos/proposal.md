# Proposal

**Issue:** ISSUE-001 - Diseñar base de datos y modelos (Sprint 1)
**Requisitos relacionados:** RF-03, RF-07, RF-08, RF-10, RNF-03, RNF-05, RNF-09
**Depende de:** `configurar-entorno-desarrollo` (ISSUE-000) aplicado.

## Why

Todas las funcionalidades de GestorCar (autenticación, vehículos, gastos,
evidencias, historial e informes) trabajan sobre las mismas entidades. Definir
el modelo de datos completo al inicio evita migraciones conflictivas entre
integrantes y permite crear el modelo de usuario propio antes de la primera
migración, que en Django no se puede cambiar después sin rehacer la base de
datos.

El equipo propuso un modelo inicial (vehículos, usuarios, registros,
evidencias y una posible entidad de gastos). Este cambio lo valida contra los
requisitos y lo completa.

## What Changes

- Una sola app de Django, `gestorcar`, organizada por capas MVC: `models/`
  (un archivo por entidad), `controllers/`, `views/` (plantillas), `forms/`,
  `admin/` y `tests/`.
- Modelo de usuario propio que se identifica por correo, con nombre y
  apellido; se configura como modelo de autenticación del proyecto.
- Modelo de vehículo con marca, modelo, año, placa, kilometraje, tipo y estado
  (activo o retirado), perteneciente a un usuario.
- Modelo de categoría con su tipo de actividad (la carga del catálogo es
  ISSUE-004).
- Modelo de registro de gasto o intervención con fecha, categoría, descripción,
  costo y kilometraje, perteneciente a un vehículo.
- Modelo de evidencia con el archivo adjunto y su tipo (factura, fotografía,
  cotización o comprobante), perteneciente a un registro.
- Restricciones de integridad en la base de datos: unicidad, valores no
  negativos y protección del historial frente a borrados.
- Registro de los modelos en el administrador de Django y pruebas de las
  restricciones.

Ajustes respecto a la propuesta del equipo:
- **Se agregan:** año, placa, estado y dueño del vehículo (RF-03, RF-06); el
  vehículo de cada registro; la entidad categoría (RF-09); el tipo de cada
  evidencia y la posibilidad de adjuntar documentos además de fotos (RF-10).
- **Se quita:** la edad del usuario, porque ningún requisito la usa y quedaría
  desactualizada con el tiempo.
- **No se crea una entidad "Gastos":** el registro ya es el gasto o la
  intervención (RF-07), y los totales se calculan a partir de los registros
  (RF-19, RNF-06) en lugar de guardarse.

## Capabilities

### New Capabilities
- `integridad-datos`: reglas que la base de datos garantiza sobre usuarios,
  vehículos, categorías, registros y evidencias — pertenencia, unicidad,
  valores válidos y conservación del historial.

### Modified Capabilities
<!-- No hay especificaciones existentes en openspec/specs/. -->

## Impact

- **Código nuevo:** app `gestorcar` con los modelos en `gestorcar/models/`,
  una migración inicial única, registro en el admin y pruebas.
- **Configuración:** `AUTH_USER_MODEL = "gestorcar.Usuario"` e inclusión de
  `gestorcar` en `INSTALLED_APPS`.
- **Base de datos:** primeras migraciones del proyecto; requiere PostgreSQL de
  ISSUE-000.
- **Equipo:** ISSUE-002 a ISSUE-007 construyen sus vistas sobre estos modelos.
  Cambiar un campo después implica una migración nueva coordinada.
- **Fuera de alcance:** vistas y formularios (ISSUE-002, 003, 005, 006), carga
  del catálogo de categorías (ISSUE-004) y almacenamiento de archivos
  (ISSUE-006).

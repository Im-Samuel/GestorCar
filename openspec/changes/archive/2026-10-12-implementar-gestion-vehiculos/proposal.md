# Proposal

**Issue:** ISSUE-003 - Implementar gestión de vehículos (Sprint 1)
**Requisitos relacionados:** RF-03, RF-04, RF-05, RF-06, RNF-02, RNF-07, RNF-09, RNF-13, RNF-15
**Depende de:** `disenar-modelos-datos` (ISSUE-001) e `implementar-autenticacion` (ISSUE-002) aplicados.

## Why

El vehículo es el centro de GestorCar: cada gasto, evidencia, historial e
informe cuelga de uno. Con el modelo y la autenticación listos, el usuario
necesita poder registrar sus vehículos, consultarlos, mantener su kilometraje al
día y retirarlos sin perder su historial. Con esto se cierra el Sprint 1.

## What Changes

- Pantallas para registrar, listar, ver el detalle, editar y retirar vehículos
  del usuario autenticado.
- Validaciones de negocio con mensajes junto a cada campo: año dentro de un
  rango válido, placa única entre los vehículos del usuario, kilometraje no
  negativo y campos obligatorios.
- Retiro lógico con confirmación: el vehículo pasa a "retirado" y conserva su
  historial; no existe opción para eliminarlo.
- La página de inicio pasa a ser el listado de vehículos del usuario.
- Enlace "Mis vehículos" en la barra de navegación.

## Capabilities

### New Capabilities
- `gestion-vehiculos`: registro, consulta, actualización y retiro de los
  vehículos de un usuario.

### Modified Capabilities
<!-- `autenticacion` no cambia sus requisitos; solo se reutiliza. -->

## Impact

- **Código nuevo:** formulario, controladores, rutas y plantillas de vehículos
  en las capas de `gestorcar/` (`forms/`, `controllers/`, `urls/` y `views/`);
  validación de año en `Vehiculo.clean()`.
- **Código modificado:** la URL `/` apunta al listado de vehículos; la barra de
  navegación de `gestorcar/views/base.html` incluye "Mis vehículos".
- **Base de datos:** sin migraciones nuevas.
- **Fuera de alcance:** historial de gastos dentro del detalle (ISSUE-008),
  reactivar un vehículo retirado y eliminarlo físicamente.

# Tasks

## 1. Validación del modelo y formulario

- [x] 1.1 Agregar a `Vehiculo.clean()` las reglas de año mínimo (1900) y máximo (año actual más uno) con mensajes en español asociados al campo año, sin crear migraciones; verificar con prueba el escenario "Validación fuera del formulario"
- [x] 1.2 Crear `VehiculoForm` con normalización y unicidad de placa por usuario (excluyendo el propio vehículo al editar); verificar con pruebas los escenarios "Placa repetida", "Año fuera de rango" y "Kilometraje negativo"

## 2. Registrar y consultar

- [x] 2.1 Crear las vistas `lista` y `detalle` con `PropietarioMixin`, sus URLs y el orden activos primero; verificar con pruebas los escenarios "Listado con vehículos activos y retirados", "Sin vehículos" y "Listado sin vehículos ajenos"
- [x] 2.2 Crear la vista `crear` que asigna el usuario autenticado antes de validar y captura `IntegrityError` de placa; verificar con pruebas los escenarios "Registro válido" y "Varios vehículos"
- [x] 2.3 Crear las plantillas `lista.html` (tabla en escritorio, tarjetas en teléfono), `detalle.html` y `formulario.html` con `includes/campo.html`; verificar que se ven sin desplazamiento horizontal a 360 píxeles de ancho y que los errores aparecen junto a cada campo
- [x] 2.4 Redirigir `/` al listado y agregar "Mis vehículos" a la barra de navegación; verificar con prueba el escenario "Página de inicio"

## 3. Actualizar

- [x] 3.1 Crear la vista `editar` reutilizando `VehiculoForm` y `formulario.html`; verificar con pruebas los escenarios "Formulario precargado" y "Actualizar kilometraje" (con un registro asociado creado desde el modelo)

## 4. Retirar

- [x] 4.1 Crear la vista `retirar` (`GET` confirma, `POST` retira) y `confirmar_retiro.html`; verificar con pruebas los escenarios "Retiro confirmado" y "Retiro sin confirmar", y que un `GET` no cambia el estado
- [x] 4.2 Verificar con prueba que no existe ninguna URL ni botón para eliminar un vehículo

## 5. Aislamiento e integración

- [x] 5.1 Verificar con pruebas el escenario "Acceso a vehículo ajeno" para detalle, edición y retiro (respuesta 404 y vehículo sin cambios)
- [x] 5.2 Recorrer manualmente registrar, listar, editar y retirar solo con el teclado en escritorio y en modo teléfono; verificar que `docker compose run --rm web pytest` pasa completo

## Workflow follow-up

- Archivar el cambio con `/opsx:archive` después de fusionarlo.
- Marcar ISSUE-003 como terminado en `docs/Issues/Issues.md` y cerrar el Sprint 1.

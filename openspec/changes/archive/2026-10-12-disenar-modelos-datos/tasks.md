# Tasks

## 1. Estructura de la app

- [x] 1.1 Crear la app `gestorcar` organizada por capas (`models/`, `controllers/`, `views/`, `forms/`, `admin/`, `migrations/`, `tests/`) y agregarla a `INSTALLED_APPS`; verificar que `python manage.py check` no reporta errores

## 2. Usuario

- [x] 2.1 Crear `Usuario` (hereda de `AbstractUser`, sin `username`, `USERNAME_FIELD = "email"`) y `UsuarioManager` con `create_user` y `create_superuser` que normalizan el correo; configurar `AUTH_USER_MODEL = "gestorcar.Usuario"`; verificar que `python manage.py createsuperuser` pide correo y no nombre de usuario
- [x] 2.2 Agregar el `UniqueConstraint` sobre `Lower("email")` y registrar `Usuario` en el admin; verificar con pruebas los escenarios "Correo repetido con distinta capitalización" y "Contraseña almacenada"

## 3. Vehículo

- [x] 3.1 Crear `Vehiculo` con sus campos, `TextChoices` de tipo y estado, `PROTECT` hacia `Usuario`, restricción `anio >= 1900` y `UniqueConstraint` en (`usuario`, `placa`); verificar con pruebas los escenarios "Vehículo sin dueño" y "Vehículo nuevo"
- [x] 3.2 Normalizar la placa en `save()` y `clean()`; verificar con pruebas los escenarios "Placa repetida para el mismo usuario" y "Misma placa en usuarios distintos"
- [x] 3.3 Registrar `Vehiculo` en el admin con filtros por estado y tipo; verificar que se puede crear un vehículo desde `/admin/`

## 4. Categoría, registro y evidencia

- [x] 4.1 Crear `Categoria` con nombre único y `tipo_actividad`; verificar con prueba el escenario "Categoría duplicada"
- [x] 4.2 Crear `Registro` con `PROTECT` hacia `Vehiculo` y `Categoria`, `costo` decimal con `CheckConstraint >= 0`, kilometraje no negativo e índice (`vehiculo`, `fecha`); verificar con pruebas los escenarios "Registro huérfano", "Costo negativo", "Kilometraje negativo" y "Costo cero"
- [x] 4.3 Crear `Evidencia` con `CASCADE` hacia `Registro`, `archivo`, `tipo` y `nombre_original`; verificar con prueba el escenario "Eliminar un registro con evidencias"
- [x] 4.4 Registrar `Categoria`, `Registro` y `Evidencia` en el admin (evidencias en línea dentro del registro); verificar que se puede crear un registro con una evidencia desde `/admin/`

## 5. Historial y transacciones

- [x] 5.1 Verificar con pruebas los escenarios "Eliminar un vehículo con historial" y "Eliminar una categoría en uso" (se lanza `ProtectedError` y los datos se conservan)
- [x] 5.2 Activar `ATOMIC_REQUESTS = True` en la configuración de la base de datos; verificar con prueba el escenario "Fallo a mitad de una operación" usando `transaction.atomic()`

## 6. Migraciones e integración

- [x] 6.1 Generar la migración inicial única de `gestorcar`; verificar que `python manage.py migrate` funciona sobre una base de datos vacía y que `python manage.py makemigrations --check` no detecta cambios pendientes
- [x] 6.2 Documentar en `README.md` el diagrama de entidades y la regla de coordinar cambios de modelos en el equipo; verificar que `docker compose run --rm web pytest` pasa completo

## Workflow follow-up

- Archivar el cambio con `/opsx:archive` después de fusionarlo, para que `integridad-datos` pase a `openspec/specs/`.
- Marcar ISSUE-001 como terminado en `docs/Issues/Issues.md`.

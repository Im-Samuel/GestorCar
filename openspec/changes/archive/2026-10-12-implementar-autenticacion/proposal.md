# Proposal

**Issue:** ISSUE-002 - Implementar registro y autenticación de usuarios (Sprint 1)
**Requisitos relacionados:** RF-01, RF-02, RNF-01, RNF-02, RNF-03, RNF-13, RNF-14, RNF-15
**Depende de:** `disenar-modelos-datos` (ISSUE-001) aplicado.

## Why

Todos los datos de GestorCar pertenecen a una persona, así que antes de
gestionar vehículos o gastos alguien tiene que poder crear su cuenta, entrar y
salir, y el sistema tiene que garantizar que cada usuario vea solo lo suyo.
Además, es el primer cambio con pantallas: aquí se define la plantilla base que
reutilizarán todas las vistas siguientes.

## What Changes

- Página de registro de cuenta (nombre, apellido, correo, contraseña y
  confirmación) que inicia sesión al terminar.
- Inicio y cierre de sesión con correo y contraseña.
- Protección por defecto: toda página requiere sesión salvo las de registro e
  inicio de sesión.
- Mecanismo común para limitar las consultas al usuario autenticado, que
  usarán vehículos, gastos e historial.
- Plantilla base de la interfaz: barra de navegación, mensajes del sistema,
  diseño adaptable con Tailwind CSS y formularios accesibles que muestran los
  errores junto a cada campo.
- Página de inicio provisional para usuarios autenticados.

## Capabilities

### New Capabilities
- `autenticacion`: creación de cuentas, inicio y cierre de sesión, acceso
  protegido y aislamiento de los datos entre usuarios.

### Modified Capabilities
<!-- No hay especificaciones existentes que cambien. -->

## Impact

- **Código nuevo:** controladores en `gestorcar/controllers/`, formularios en
  `gestorcar/forms/`, rutas en `gestorcar/urls/` y plantillas en
  `gestorcar/views/`; mezcla (mixin) de aislamiento por usuario.
- **Configuración:** middleware de sesión obligatoria, `LOGIN_URL`,
  `LOGIN_REDIRECT_URL`, `LOGOUT_REDIRECT_URL`, carpeta de plantillas `gestorcar/views/` y
  `STATICFILES_DIRS`.
- **Dependencias externas:** `tailwindcss`, `@tailwindcss/cli` y
  `@tailwindcss/forms` como dependencias de npm en el `package.json`
  existente; el CSS se compila a un archivo estático y no se agregan paquetes
  de Python.
- **Infraestructura:** servicio `tailwind` en `docker-compose.yml` que
  recompila el CSS al guardar plantillas.
- **Equipo:** las vistas de ISSUE-003 en adelante heredan la plantilla base y
  el mecanismo de aislamiento.
- **Fuera de alcance:** recuperación de contraseña por correo, edición del
  perfil, inicio de sesión con redes sociales y verificación del correo.

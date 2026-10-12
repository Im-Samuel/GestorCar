# Tasks

## 1. Configuración

- [x] 1.1 Agregar `LoginRequiredMiddleware`, `LOGIN_URL`, `LOGIN_REDIRECT_URL`, `LOGOUT_REDIRECT_URL` y la carpeta de plantillas `gestorcar/views/` en `TEMPLATES["DIRS"]`; incluir `gestorcar/urls/cuentas.py` desde `config/urls.py`; verificar que `python manage.py check` no reporta errores

## 2. Interfaz base (frontend)

- [x] 2.1 Agregar `tailwindcss`, `@tailwindcss/cli` y `@tailwindcss/forms` a `package.json` con los scripts `css:build` y `css:watch`, crear `static/src/app.css` (`@import "tailwindcss"`, `@plugin "@tailwindcss/forms"` y las clases de `@layer components`), configurar `STATICFILES_DIRS` y excluir `static/css/app.css` en `.gitignore`; verificar que `npm run css:build` genera `static/css/app.css` y que `git status` no lo muestra
- [x] 2.2 Agregar a `docker-compose.yml` el servicio `tailwind` (`node:24-alpine`, ejecuta `npm ci && npm run css:watch` sobre el proyecto montado); verificar que con `docker compose up` una clase nueva agregada a una plantilla aparece en `static/css/app.css` sin reiniciar nada
- [x] 2.3 Crear `gestorcar/views/base.html` que cargue `{% static 'css/app.css' %}`, con barra de navegación adaptable (menú con `<details>`/`<summary>` en teléfono), zona de mensajes y bloque de contenido; verificar que la página se ve sin desplazamiento horizontal a 360 píxeles de ancho y que el menú se abre con el teclado
- [x] 2.4 Crear `gestorcar/views/includes/campo.html` con etiqueta, marca de obligatorio, ayuda y errores enlazados por `aria-describedby` y `aria-invalid`, usando las clases `.campo` y `.campo-error`; verificar con una prueba que un campo con error renderiza esos atributos
- [x] 2.5 Crear la vista y plantilla `inicio` en `/`; verificar con prueba que un usuario con sesión la ve y uno sin sesión es redirigido a inicio de sesión

## 3. Registro de cuenta

- [x] 3.1 Crear `RegistroForm` (nombre, apellido, correo, contraseña y confirmación) que rechace correos existentes sin distinguir mayúsculas; verificar con pruebas los escenarios "Correo ya registrado", "Contraseñas distintas", "Contraseña débil" y "Campos obligatorios vacíos"
- [x] 3.2 Crear la vista, URL y plantilla de registro (marcada `login_not_required`) que inicia sesión al guardar; verificar con prueba el escenario "Registro exitoso"

## 4. Inicio y cierre de sesión

- [x] 4.1 Configurar `LoginView` con el formulario por correo y su plantilla; verificar con pruebas los escenarios "Credenciales válidas", "Credenciales inválidas" y "Regreso a la página solicitada"
- [x] 4.2 Configurar `LogoutView` y el botón de cierre de sesión por `POST` en la barra de navegación; verificar con pruebas los escenarios "Cerrar sesión" y "Página protegida después de salir"
- [x] 4.3 Redirigir a inicio cuando un usuario con sesión abre registro o inicio de sesión; verificar con prueba el escenario "Usuario con sesión abre registro o inicio de sesión"

## 5. Protección y aislamiento

- [x] 5.1 Verificar con prueba el escenario "Página nueva sin configuración adicional" usando una vista de prueba sin decoradores
- [x] 5.2 Crear `PropietarioMixin` en `gestorcar/controllers/mixins.py`; verificar con prueba el escenario "Dato de otra cuenta" (respuesta 404) usando dos usuarios y un vehículo creado directamente con el modelo

## 6. Documentación y verificación

- [x] 6.1 Documentar en `README.md` la estructura de plantillas, el uso de `includes/campo.html` y de `PropietarioMixin` para las vistas siguientes, los comandos de Tailwind (`npm run css:watch`, `npm run css:build`), las clases de componentes disponibles y la regla de escribir siempre nombres de clase completos; verificar que la sección explica cómo crear una vista protegida nueva con estilos
- [x] 6.2 Recorrer manualmente registro, inicio y cierre de sesión solo con el teclado en navegador de escritorio y en modo teléfono; verificar que todos los controles son alcanzables y que `docker compose run --rm web pytest` pasa completo

## Workflow follow-up

- Archivar el cambio con `/opsx:archive` después de fusionarlo.
- Marcar ISSUE-002 como terminado en `docs/Issues/Issues.md`.

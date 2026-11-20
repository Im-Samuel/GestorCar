# Design

## Context

`disenar-modelos-datos` deja creado `gestorcar.Usuario` (inicio de sesión por
correo, `first_name`, `last_name`) y `LANGUAGE_CODE = "es"` viene de ISSUE-000,
por lo que los mensajes de validación de Django ya salen en español. No existe
ninguna plantilla ni vista. Ver `proposal.md` y `specs/autenticacion/spec.md`.

En Django, el patrón MVC del backlog se llama MTV:

| Backlog (MVC) | Django | Dónde vive |
|---|---|---|
| Modelo | Model | `gestorcar/models/` |
| Controlador | View + URL | `gestorcar/controllers/`, `gestorcar/urls/` |
| Vista | Template (+ Form) | `gestorcar/views/`, `gestorcar/forms/` |

Archivos de este cambio: controladores en `gestorcar/controllers/cuentas.py` e
`inicio.py`, formularios en `gestorcar/forms/cuentas.py` y rutas en
`gestorcar/urls/cuentas.py` (espacio de nombres `cuentas`), incluidas desde
`config/urls.py`.

Este cambio incluye las tres capas: no hay un frontend separado, las pantallas
son plantillas que Django renderiza en el servidor.

## Goals / Non-Goals

**Goals:**
- Que la seguridad sea la opción por defecto: una vista nueva queda protegida
  sin que nadie tenga que acordarse de protegerla.
- Una plantilla base y un patrón de formularios que el resto del equipo copie
  sin repensar el diseño.

**Non-Goals:**
- Recuperación de contraseña, edición de perfil y verificación de correo.
- Un sistema de diseño propio; se usan las utilidades y la paleta por defecto
  de Tailwind, sin tema personalizado.

## Decisions

### 1. Vistas de autenticación de Django
- Inicio de sesión: `LoginView` con un `AuthenticationForm` cuyo campo se
  rotula "Correo electrónico", y `redirect_authenticated_user=True`.
- Cierre de sesión: `LogoutView`, que en Django 5 solo acepta `POST`; el botón
  de la barra de navegación es un pequeño formulario con token CSRF.
- Registro: `CreateView` con `RegistroForm` (subclase de `UserCreationForm`
  con `first_name`, `last_name` y `email` obligatorios) que, al guardar, llama
  a `login()` y redirige a inicio.
- **Alternativa:** `django-allauth`; aporta recuperación por correo y redes
  sociales que no se piden, a cambio de mucha configuración.

### 2. Sesión obligatoria con `LoginRequiredMiddleware`
Se agrega `django.contrib.auth.middleware.LoginRequiredMiddleware` (Django
5.1+). Toda vista exige sesión salvo las marcadas con `login_not_required`
(registro; `LoginView` ya lo está). `LOGIN_URL = "cuentas:iniciar_sesion"`,
`LOGIN_REDIRECT_URL = "inicio"`, `LOGOUT_REDIRECT_URL = "cuentas:iniciar_sesion"`.
- **Alternativa:** `LoginRequiredMixin` en cada vista; basta con olvidarlo una
  vez para exponer datos (RNF-01).

### 3. Aislamiento con `PropietarioMixin`
`gestorcar/controllers/mixins.py` define `PropietarioMixin`, que filtra `get_queryset()` por
`{campo_propietario: request.user}`. El campo es `"usuario"` en vehículos y
`"vehiculo__usuario"` en registros. Como `get_object()` parte de ese
`queryset`, un dato ajeno produce 404 (no 403), sin revelar que existe.
- **Alternativa:** comprobar el dueño en cada vista; repetido y fácil de
  olvidar. Un middleware no puede hacerlo porque no conoce el modelo.

### 4. Plantillas
- Carpeta de plantillas `gestorcar/views/` (declarada en `TEMPLATES["DIRS"]`)
  con `base.html`: barra de
  navegación adaptable (nombre del usuario y "Cerrar sesión" con sesión;
  "Iniciar sesión" y "Crear cuenta" sin ella), mensajes de `django.contrib.messages`
  y bloque de contenido. Carga el CSS con `{% static 'css/app.css' %}`.
- `gestorcar/views/includes/campo.html` dibuja un campo con su etiqueta, marca de
  obligatorio, texto de ayuda y errores enlazados con `aria-describedby` e
  `aria-invalid`. Todos los formularios del proyecto lo reutilizan.
- Plantillas de autenticación en `gestorcar/views/cuentas/`.
- **Alternativa:** `django-crispy-forms`; ahorra marcado pero añade una
  dependencia y oculta el HTML que el equipo debe aprender a ajustar.

### 5. Tailwind CSS 4 compilado con npm
`tailwindcss`, `@tailwindcss/cli` y `@tailwindcss/forms` se agregan como
dependencias de desarrollo al `package.json` que ya existe para OpenSpec. El
origen `static/src/app.css` contiene `@import "tailwindcss";` y
`@plugin "@tailwindcss/forms";`, y se compila a `static/css/app.css`, que se
sirve con `STATICFILES_DIRS = [BASE_DIR / "static"]` y queda fuera de git por
ser un archivo generado. Tailwind 4 detecta automáticamente las clases usadas
en las plantillas del proyecto (respeta `.gitignore`, así que no revisa
`node_modules` ni `.venv`).

Scripts de npm: `css:build` (compila minificado una vez) y `css:watch`
(recompila al guardar). En Docker, un servicio `tailwind` con la imagen
`node:24-alpine` ejecuta `npm ci && npm run css:watch` sobre el proyecto
montado; en local basta con `npm run css:watch`.
- **Alternativa: Play CDN de Tailwind.** Una línea en `base.html`, pero genera
  el CSS en el navegador en cada carga y Tailwind lo indica solo para
  prototipos.
- **Alternativa: `django-tailwind`.** Agrega una app y comandos de
  `manage.py`, pero es otra dependencia de Python y necesita Node igualmente.
- **Alternativa: ejecutable independiente de Tailwind.** No requiere Node,
  pero cada sistema operativo necesita un binario distinto, y el equipo ya usa
  Node para OpenSpec.

### 6. Componentes reutilizables y menú sin JavaScript
- En `static/src/app.css`, dentro de `@layer components`, se definen con
  `@apply` las clases repetidas del proyecto (`.btn`, `.btn-primario`,
  `.btn-secundario`, `.campo`, `.campo-error`, `.tarjeta`), para que las
  plantillas no repitan largas listas de utilidades y el estilo se ajuste en un
  solo lugar.
- El menú de la barra de navegación en teléfono usa `<details>` y `<summary>`
  con clases `md:` para mostrarse abierto en pantallas grandes. Funciona con
  teclado y sin JavaScript (Bootstrap traía su propio JavaScript para esto).

### 7. Página de inicio provisional
Controlador `inicio` en `gestorcar/controllers/inicio.py` que saluda al
usuario. ISSUE-003 la
reemplazará por el listado de vehículos o un panel.

### 8. URLs
| URL | Nombre | Vista |
|---|---|---|
| `/` | `inicio` | página de inicio |
| `/cuentas/registro/` | `cuentas:registro` | registro |
| `/cuentas/iniciar-sesion/` | `cuentas:iniciar_sesion` | inicio de sesión |
| `/cuentas/cerrar-sesion/` | `cuentas:cerrar_sesion` | cierre de sesión |

## Risks / Trade-offs

- [Si el servicio `tailwind` no está corriendo, las páginas se ven sin
  estilos o con clases nuevas sin aplicar] → `docker compose up` lo levanta
  junto con la aplicación y el `README.md` explica `npm run css:watch` para
  trabajar en local.
- [Tailwind no detecta clases construidas por partes, como `"bg-" + color`] →
  Escribir siempre el nombre completo de cada clase en plantillas y Python;
  queda documentado en el `README.md`.
- [`LoginRequiredMiddleware` también protege el admin y archivos estáticos en
  desarrollo] → El admin ya exige sesión; `runserver` sirve los estáticos
  antes del middleware. Se verifica con una prueba.
- [Mensajes de error que revelan si un correo existe al registrarse] →
  Aceptado: el registro necesita indicar que el correo está en uso; el inicio
  de sesión sí usa un mensaje general.

## Migration Plan

Sin migraciones de base de datos. Reversión: revertir el commit.

## Open Questions

- Contenido definitivo de la página de inicio; se decide en ISSUE-003 sin
  afectar esta especificación.

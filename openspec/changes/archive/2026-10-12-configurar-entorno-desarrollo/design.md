# Design

## Context

El proyecto es un esqueleto de `django-admin startproject` (Django 5.2.17) sin
apps propias: `config/settings.py` tiene `SECRET_KEY` y `DEBUG = True` fijos,
usa SQLite y `LANGUAGE_CODE = "en-us"`. Ver `proposal.md` (Why) para la
motivación.

Restricciones observadas:
- El equipo trabaja principalmente en Windows y la configuración de git
  convierte los finales de línea a CRLF, pero los contenedores son Linux.
- Las versiones de Python locales varían: el `venv` original usaba 3.11.9 y al
  menos un equipo tiene 3.14 como versión por defecto.
- Docker 29 ya está disponible en al menos un equipo del equipo.
- El repositorio está en GitHub (`Im-Samuel/GestorCar`).
- OpenSpec se instala con npm (`package.json`), fuera de la imagen de Python.

## Goals / Non-Goals

**Goals:**
- Que `docker compose up` sea la forma de referencia de levantar el proyecto,
  idéntica en todos los equipos.
- Mantener una alternativa local (entorno virtual) para quien prefiera ejecutar
  Django fuera del contenedor, compartiendo la misma base de datos en Docker.
- Un único archivo de configuración legible, sin dividir en módulos por entorno.

**Non-Goals:**
- Despliegue a producción (servidor WSGI, archivos estáticos con un servidor
  dedicado, HTTPS). Se abordará en un cambio posterior.
- Almacenamiento de archivos subidos (`media/`); llega con ISSUE-006.
- Respaldo y recuperación de la base de datos; corresponde a ISSUE-017.
- Gestores de dependencias avanzados (Poetry, uv, pip-tools).
- Integración continua con GitHub Actions; está pendiente de validar con el
  equipo (ver Open Questions).

## Decisions

### 1. PostgreSQL 17 como motor de base de datos
Se reemplaza SQLite por PostgreSQL 17 (imagen `postgres:17-alpine`) con un
volumen con nombre (`postgres_data`).
- **Por qué:** el proyecto se evalúa en BD por relaciones e integridad;
  PostgreSQL aplica claves foráneas y restricciones de forma estricta, soporta
  bien las agregaciones de los informes (RNF-10, RNF-11) y es el motor que se
  usaría al desplegar.
- **Alternativas:** SQLite (cero configuración, pero un archivo por equipo,
  concurrencia limitada y comportamiento distinto al de producción); MySQL
  (válido, pero sin ventaja para este caso y con integración menos directa en
  Django).

### 2. `django-environ` para leer la configuración
`settings.py` usa `environ.Env` para leer `.env` y convertir tipos
(`DEBUG` como booleano, `ALLOWED_HOSTS` como lista, `DATABASE_URL` como
diccionario de conexión). `SECRET_KEY` y `DATABASE_URL` no tienen valor por
defecto, por lo que su ausencia detiene el arranque con `ImproperlyConfigured`
(escenario "Variable obligatoria ausente"). `DEBUG` tiene `False` por defecto.
- **Alternativas:** `os.environ` (obliga a convertir tipos y armar la URL de la
  base de datos a mano); `python-decouple` (similar, pero sin parseo de
  `DATABASE_URL` integrado, que requeriría además `dj-database-url`).

### 3. Python 3.11 fijado en la imagen
La imagen base es `python:3.11-slim` y se agrega `.python-version` con `3.11`
para quien trabaje en local (`py -3.11 -m venv .venv` en Windows).
- **Por qué:** es la versión con la que el equipo ya creó el entorno y Django
  5.2 la soporta; dentro de Docker la versión local deja de importar.
- **Alternativa:** 3.13. Se puede subir más adelante cambiando solo la imagen
  base y `.python-version`.

### 4. Servidor de desarrollo y arranque sin script de entrada
El servicio `web` ejecuta
`sh -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"`
y depende del servicio `db` con `condition: service_healthy`, cuyo healthcheck
es `pg_isready`. El código se monta como volumen (`.:/app`) para que los cambios
se recarguen sin reconstruir la imagen.
- **Por qué no un `entrypoint.sh`:** en Windows git lo convertiría a CRLF y
  fallaría dentro del contenedor Linux; la orden en línea evita el problema.
- **Alternativa:** un script de espera (`wait-for-it`); innecesario con el
  healthcheck nativo de Compose.

### 5. Desarrollo local opcional contra la base de datos en Docker
Quien no quiera ejecutar Django en el contenedor levanta solo la base de datos
(`docker compose up db`) y usa un `.venv` local con
`DATABASE_URL=postgres://...@localhost:5432/...`. El puerto publicado es
configurable con `DB_PORT` (por defecto 5432).

### 6. Dependencias en dos archivos
`requirements.txt` (ejecución: Django, `django-environ`, `psycopg[binary]`) y
`requirements-dev.txt` (`-r requirements.txt` más `ruff`, `pytest`,
`pytest-django`), ambos en UTF-8 y con versiones exactas. La imagen instala
`requirements-dev.txt` porque es una imagen de desarrollo.

### 7. Calidad: `ruff` y `pytest-django` configurados en `pyproject.toml`
`ruff` actúa como linter y formateador; `pytest` con `pytest-django` es el
comando único de pruebas (`docker compose run --rm web pytest`). Se agrega una
prueba de humo en `tests/` que verifica la conexión a PostgreSQL y que no haya
migraciones pendientes, para que la suite nunca esté vacía (pytest falla si no
recoge pruebas).
- **Alternativas:** `flake8` + `black` + `isort` (tres herramientas en lugar de
  una); `python manage.py test` (sin dependencias extra, pero con salida y
  fixtures menos cómodas que pytest).

### 8. Finales de línea normalizados con `.gitattributes`
Se agrega `* text=auto eol=lf` y se renormaliza el repositorio una vez. Los
editores en Windows manejan LF sin problema y se eliminan los avisos de
conversión y los fallos en contenedores.

### 9. Idioma y zona horaria
`LANGUAGE_CODE = "es"`. `TIME_ZONE` se lee del entorno con `UTC` por defecto;
`USE_TZ` sigue activo, por lo que las fechas se guardan en UTC.

## Risks / Trade-offs

- [Docker Desktop en Windows es lento con volúmenes montados] → Se recomienda
  clonar el repositorio dentro de WSL2; la alternativa local (decisión 5)
  sigue disponible.
- [El puerto 5432 ya está ocupado por un PostgreSQL instalado localmente] →
  `DB_PORT` configurable en `.env`.
- [La renormalización de finales de línea genera un diff grande una sola vez] →
  Hacerla en un commit separado y avisar al equipo para que actualice sus ramas.
- [Integrantes sin Docker no pueden levantar el proyecto] → Docker pasa a ser
  requisito documentado en el `README.md`.
- [La imagen de desarrollo incluye herramientas que no van a producción] →
  Aceptado; el despliegue es un no-objetivo de este cambio.

## Migration Plan

1. Fusionar el cambio en `main`.
2. Cada integrante actualiza su copia, borra su antiguo `venv/` y su
   `db.sqlite3` (no contienen datos de la aplicación porque aún no hay modelos),
   copia `.env.example` a `.env` y ejecuta `docker compose up`.
3. Quien tenga ramas abiertas las rebasa sobre `main` tras la renormalización.
4. **Reversión:** revertir el commit restaura la configuración con SQLite; no
   hay datos que migrar en ningún sentido.

## Open Questions

- Zona horaria local del equipo para `TIME_ZONE` en `.env.example`; se puede
  ajustar en cualquier momento sin cambiar la especificación.
- ¿Adoptar GitHub Actions para ejecutar linter y pruebas en cada pull request?
  Pendiente de validar con el equipo. Si se aprueba, será un cambio propio (por
  ejemplo `agregar-integracion-continua`) y no afecta a este.

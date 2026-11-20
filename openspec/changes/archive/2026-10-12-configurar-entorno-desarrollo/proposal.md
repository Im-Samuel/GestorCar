# Proposal

**Issue:** ISSUE-000 - Configurar entorno de desarrollo y colaboración (Sprint 0)
**Requisitos relacionados:** RNF-03, RNF-19, RNF-20, RNF-21

## Why

GestorCar lo desarrollan varias personas en equipos distintos, pero hoy el
proyecto no se puede levantar de forma reproducible: el entorno virtual que se
versionó fue creado en otra máquina (`C:\Users\samue\...`), `requirements.txt`
está en UTF-16, el `SECRET_KEY` está escrito en `config/settings.py` y no hay
instrucciones de instalación. Antes de empezar el Sprint 1 el equipo necesita un
entorno común, con versiones fijadas y una base de datos que soporte las
relaciones e integridad que exige el proyecto.

## What Changes

- Configuración de Django basada en variables de entorno (`SECRET_KEY`, `DEBUG`,
  `ALLOWED_HOSTS`, `DATABASE_URL`, `TIME_ZONE`), con un `.env.example`
  versionado y el `.env` real excluido del repositorio.
- Cambio del motor de base de datos de SQLite a **PostgreSQL**, ejecutado en
  Docker con un volumen persistente.
- `Dockerfile` y `docker-compose.yml` para levantar la aplicación y la base de
  datos con un solo comando, aplicando las migraciones al arrancar.
- `requirements.txt` en UTF-8 con las dependencias de ejecución y
  `requirements-dev.txt` con las de desarrollo (linter, formateador y pruebas).
- Herramientas de calidad comunes: `ruff` como linter y formateador, `pytest`
  con `pytest-django` como comando único de pruebas.
- `.gitattributes` para normalizar finales de línea entre Windows y los
  contenedores Linux.
- `README.md` con instalación con Docker y en local, uso de OpenSpec con Claude
  Code y OpenCode, y convenciones de ramas, commits y pull requests.
- Idioma de la aplicación en español (`LANGUAGE_CODE = "es"`).

## Capabilities

### New Capabilities
- `entorno-ejecucion`: cómo se configura y se ejecuta la aplicación —
  configuración por variables de entorno, manejo de secretos, base de datos
  persistente y arranque reproducible con contenedores.

### Modified Capabilities
<!-- No hay especificaciones existentes en openspec/specs/. -->

## Impact

- **Código:** `config/settings.py` deja de tener valores fijos y pasa a leerlos
  del entorno. No hay modelos ni vistas afectados porque aún no existen apps.
- **Dependencias nuevas:** `django-environ`, `psycopg` (ejecución); `ruff`,
  `pytest`, `pytest-django` (desarrollo).
- **Infraestructura:** Docker y Docker Compose pasan a ser requisito de cada
  integrante; la base de datos local SQLite se abandona.
- **Repositorio:** nuevos archivos `Dockerfile`, `docker-compose.yml`,
  `.dockerignore`, `.env.example`, `.gitattributes`, `pyproject.toml`,
  `requirements-dev.txt`; se reescribe `README.md`.
- **Equipo:** cada integrante debe crear su `.env` a partir de `.env.example`.
- **Fuera de alcance:** integración continua con GitHub Actions, pendiente de
  validar con el equipo para un cambio posterior.

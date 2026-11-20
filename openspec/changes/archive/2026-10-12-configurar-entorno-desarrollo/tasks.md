# Tasks

## 1. Higiene del repositorio

- [x] 1.1 Crear `.gitignore` que excluya `venv/`, `.venv/`, `node_modules/`, `.env`, `db.sqlite3`, `media/` y cachés, y retirar del índice `venv/` y `node_modules/`; verificar con `git ls-files | grep -E "^(venv|node_modules)/"` sin resultados
- [x] 1.2 Agregar `.gitattributes` con `* text=auto eol=lf` y ejecutar `git add --renormalize .` en un commit separado; verificar que `git status` queda limpio tras el commit y que `git ls-files --eol` muestra `i/lf` en los archivos de texto

## 2. Dependencias y herramientas de calidad

- [x] 2.1 Reescribir `requirements.txt` en UTF-8 con versiones exactas de Django 5.2, `django-environ` y `psycopg[binary]`; verificar con `file requirements.txt` que no es UTF-16
- [x] 2.2 Crear `requirements-dev.txt` (`-r requirements.txt` + `ruff`, `pytest`, `pytest-django`) y `.python-version` con `3.11`; verificar que `pip install -r requirements-dev.txt` termina sin errores en Python 3.11
- [x] 2.3 Crear `pyproject.toml` con la configuración de `ruff` (excluyendo `node_modules`, `.venv` y migraciones) y de `pytest` (`DJANGO_SETTINGS_MODULE = "config.settings"`); verificar que `ruff check .` y `ruff format --check .` pasan sobre el código actual

## 3. Configuración por variables de entorno

- [x] 3.1 Modificar `config/settings.py` para leer `SECRET_KEY`, `DEBUG` (por defecto `False`), `ALLOWED_HOSTS`, `DATABASE_URL` y `TIME_ZONE` con `django-environ`, y fijar `LANGUAGE_CODE = "es"`; verificar que `grep -n "django-insecure" config/settings.py` no devuelve resultados
- [x] 3.2 Crear `.env.example` con todas las variables, valores de ejemplo no sensibles y un comentario por variable; verificar que copiarlo a `.env` basta para arrancar y que `git status` no muestra `.env`
- [x] 3.3 Agregar pruebas en `tests/test_configuracion.py` para los escenarios "Variable obligatoria ausente" (el arranque falla nombrando `SECRET_KEY` o `DATABASE_URL`) y "Modo de depuración no indicado" (`DEBUG` es `False`); verificar que `pytest tests/test_configuracion.py` pasa

## 4. Contenedores y base de datos

- [x] 4.1 Crear `Dockerfile` basado en `python:3.11-slim` que instale `requirements-dev.txt`, y `.dockerignore` que excluya `.git`, `venv`, `.venv`, `node_modules` y `.env`; verificar con `docker compose build` sin errores
- [x] 4.2 Crear `docker-compose.yml` con el servicio `db` (`postgres:17-alpine`, volumen `postgres_data`, healthcheck `pg_isready`, puerto `${DB_PORT:-5432}`) y el servicio `web` (depende de `db` saludable, monta `.:/app`, ejecuta `migrate` y `runserver 0.0.0.0:8000`); verificar que `docker compose up` deja la aplicación respondiendo en `http://localhost:8000/admin/`
- [x] 4.3 Agregar la prueba de humo `tests/test_entorno.py` que comprueba que la conexión usa PostgreSQL y que no quedan migraciones sin aplicar; verificar con `docker compose run --rm web pytest`
- [x] 4.4 Verificar la persistencia: crear un superusuario con `docker compose run --rm web python manage.py createsuperuser`, ejecutar `docker compose down` y `docker compose up`, y comprobar que el superusuario puede iniciar sesión en `/admin/`
- [x] 4.5 Documentar en `README.md` los requisitos (Docker, Node para OpenSpec), el arranque con Docker, el desarrollo local con `.venv` contra `docker compose up db` y los comandos de linter y pruebas; verificar siguiendo los pasos tal como están escritos

## 5. Flujo de colaboración

- [x] 5.1 Documentar en `README.md` el uso de OpenSpec: `npm install`, los comandos `/opsx:propose`, `/opsx:apply` y `/opsx:archive` en Claude Code y sus equivalentes `/opsx-*` en OpenCode, y qué carpetas se versionan (`openspec/`, `.claude/`, `.opencode/`); verificar que un integrante puede listar los cambios con `npx openspec list`

## 6. Verificación integral

- [x] 6.1 En un equipo Windows distinto, clonar el repositorio desde cero y seguir únicamente el `README.md` hasta tener la aplicación en `http://localhost:8000` y `pytest` en verde; registrar cualquier paso faltante y corregir el `README.md`
- [x] 6.2 Marcar ISSUE-000 como terminado en `docs/Issues/Issues.md` comprobando cada criterio de aceptación contra lo entregado

## Workflow follow-up

- Validar con el equipo la adopción de GitHub Actions; si se aprueba, proponerla con `/opsx:propose` como cambio aparte.
- Archivar el cambio con `/opsx:archive` una vez revisado y fusionado, para que la especificación `entorno-ejecucion` pase a `openspec/specs/`.

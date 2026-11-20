# entorno-ejecucion Specification

## Purpose

Define cómo se configura y se ejecuta GestorCar para que cualquier integrante
del equipo obtenga el mismo entorno, sin secretos en el repositorio y con datos
que persisten entre reinicios.

## Requirements

### Requirement: Configuración por variables de entorno
La aplicación SHALL obtener su clave secreta, el modo de depuración, los hosts
permitidos, la conexión a la base de datos y la zona horaria desde variables de
entorno, sin valores sensibles escritos en el código fuente.

#### Scenario: Variables definidas en el archivo de entorno
- **WHEN** existe un archivo `.env` con `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS` y `DATABASE_URL`
- **THEN** la aplicación arranca usando exactamente esos valores

#### Scenario: Variable obligatoria ausente
- **WHEN** la aplicación arranca sin `SECRET_KEY` o sin `DATABASE_URL`
- **THEN** el arranque falla con un mensaje que nombra la variable que falta

#### Scenario: Modo de depuración no indicado
- **WHEN** la variable `DEBUG` no está definida
- **THEN** la aplicación se ejecuta con el modo de depuración desactivado

### Requirement: Secretos fuera del repositorio
El repositorio SHALL incluir una plantilla de variables de entorno con todas las
variables necesarias y valores de ejemplo no sensibles, y MUST excluir los
archivos de entorno reales, los entornos virtuales y las dependencias instaladas.

#### Scenario: Plantilla disponible tras clonar
- **WHEN** un integrante clona el repositorio
- **THEN** encuentra un `.env.example` que lista cada variable requerida con un valor de ejemplo

#### Scenario: Archivo de entorno real ignorado
- **WHEN** un integrante crea su `.env` y ejecuta `git status`
- **THEN** el archivo `.env` no aparece como archivo para versionar

### Requirement: Base de datos relacional persistente
La aplicación SHALL almacenar sus datos en un motor de base de datos relacional
con integridad referencial, y los datos confirmados MUST conservarse al detener
y volver a iniciar los servicios.

#### Scenario: Datos tras reiniciar los servicios
- **WHEN** se crea un registro, se detienen los servicios con `docker compose down` y se vuelven a iniciar con `docker compose up`
- **THEN** el registro sigue disponible

#### Scenario: Integridad referencial aplicada por la base de datos
- **WHEN** se intenta guardar un registro que referencia a otro inexistente
- **THEN** la base de datos rechaza la operación

### Requirement: Arranque reproducible con contenedores
El proyecto SHALL poder levantarse con un único comando que inicie la base de
datos y la aplicación, espere a que la base de datos esté lista y aplique las
migraciones pendientes antes de atender peticiones.

#### Scenario: Primer arranque en un equipo nuevo
- **WHEN** un integrante con Docker instalado copia `.env.example` a `.env` y ejecuta `docker compose up`
- **THEN** la aplicación responde en `http://localhost:8000` con todas las migraciones aplicadas

#### Scenario: Base de datos aún no disponible
- **WHEN** el contenedor de la aplicación inicia antes de que la base de datos acepte conexiones
- **THEN** la aplicación espera a que la base de datos esté lista en lugar de fallar

# Issues del proyecto GestorCar

Backlog inicial derivado de los requisitos funcionales y no funcionales del
proyecto. Los criterios de aceptación son verificables y permiten validar cada
issue durante el desarrollo.

## Convenciones

- **Prioridad:** Alta, Media o Baja.
- **Estado inicial:** Pendiente.
- **RF/RNF:** Requisitos relacionados.

---

## ISSUE-000 - Configurar entorno de desarrollo y colaboración

- **Prioridad:** Alta
- **Estado:** Terminado
- **Cambio de OpenSpec:** `configurar-entorno-desarrollo`
- **RF/RNF relacionados:** RNF-03, RNF-19, RNF-20, RNF-21

### Descripción

Dejar el proyecto listo para que cualquier integrante del equipo pueda
clonarlo, levantarlo y contribuir de la misma forma, con versiones fijadas,
configuración por variables de entorno, contenedores Docker y un flujo de
trabajo común con OpenSpec.

### Criterios de aceptación

- [x] La versión de Python (3.11) y de Django (5.2 LTS) está fijada y documentada.
- [x] `requirements.txt` está en UTF-8 y se instala sin errores con
  `pip install -r requirements.txt`.
- [x] `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS` y la conexión a la base de datos se
  leen desde variables de entorno; existe un `.env.example` versionado y el
  `.env` real está excluido del repositorio.
- [x] Se define el motor de base de datos del proyecto (se propone PostgreSQL) y
  sus datos persisten entre reinicios mediante un volumen.
- [x] Existen `Dockerfile` y `docker-compose.yml`; `docker compose up` levanta la
  aplicación y la base de datos y aplica las migraciones.
- [x] El `.gitignore` excluye entornos virtuales, `node_modules`, archivos `.env`,
  base de datos local, archivos subidos y cachés.
- [x] Se acuerda un formateador y linter de Python y un comando único para
  ejecutar las pruebas.
- [x] El `README.md` explica cómo levantar el proyecto en local y con Docker, y
  cómo usar OpenSpec con Claude Code y OpenCode.
- [x] Se documentan las convenciones de ramas, commits y pull requests del equipo.
- Pendiente de validar con el equipo: integración continua (GitHub Actions).
  Queda fuera del alcance de este issue.

### Verificación

Criterios comprobados el 2026-10-12: instalación limpia de `requirements.txt`
en Python 3.11, configuración leída del entorno, PostgreSQL 17 con datos
conservados tras `docker compose down` y `up`, servicios `db`, `web` y
`tailwind` levantados sin migraciones pendientes, reglas del `.gitignore`,
`ruff` y `pytest` en verde, y secciones del `README.md`. La base de datos vive
en un volumen de Docker, por lo que no queda ningún archivo de base de datos
local que excluir.

---

## ISSUE-001 - Diseñar base de datos y modelos

- **Prioridad:** Alta
- **Estado:** Pendiente
- **RF/RNF relacionados:** RF-03, RF-07, RF-08, RF-10, RNF-03, RNF-05, RNF-09
- **Dependencias:** ISSUE-000

### Descripción

Diseñar e implementar todos los modelos de datos del sistema (usuario,
vehículo, registro de gasto o intervención, categoría y evidencia), sus
relaciones y las restricciones de integridad en la base de datos. Las vistas
y formularios de cada funcionalidad se implementan en sus propios issues sobre
estos modelos.

### Criterios de aceptación

- Existe un modelo de usuario propio, creado antes de la primera migración, que
  se identifica por correo electrónico y almacena la contraseña con hash.
- El vehículo almacena marca, modelo, año, placa, kilometraje, tipo y estado
  (activo o retirado), y pertenece a un usuario.
- La placa es única por usuario.
- El registro de gasto o intervención almacena fecha, categoría, descripción,
  costo y kilometraje, y pertenece a un vehículo.
- La base de datos rechaza costos y kilometrajes negativos.
- Cada evidencia pertenece a un registro.
- No se pueden crear registros huérfanos, y no se puede eliminar un vehículo
  que tenga historial.
- Una operación inválida no deja datos guardados parcialmente.
- Las migraciones se aplican desde una base de datos vacía sin errores y los
  modelos están disponibles en el administrador de Django.
- Existen pruebas de las restricciones de integridad.

---

## ISSUE-002 - Implementar registro y autenticación de usuarios

- **Prioridad:** Alta
- **Estado:** Pendiente
- **RF/RNF relacionados:** RF-01, RF-02, RNF-01, RNF-02, RNF-03
- **Dependencias:** ISSUE-001

### Descripción

Crear las vistas, formularios y URLs para registrar usuarios, iniciar sesión y
cerrar sesión con el modelo de usuario de ISSUE-001, junto con el mecanismo
común que limita cada consulta a los datos del usuario autenticado.

### Criterios de aceptación

- Se puede crear una cuenta con los datos obligatorios.
- No se permite registrar dos cuentas con el mismo correo.
- Un usuario registrado puede iniciar y cerrar sesión.
- Las vistas protegidas redirigen al inicio de sesión cuando no hay sesión
  activa.
- Las credenciales no se almacenan en texto plano.
- Un usuario no puede consultar ni modificar información de otra cuenta.
- Se muestran mensajes claros cuando las credenciales son inválidas o faltan
  datos obligatorios.

---

## ISSUE-003 - Implementar gestión de vehículos

- **Prioridad:** Alta
- **Estado:** Pendiente
- **RF/RNF relacionados:** RF-03, RF-04, RF-05, RF-06, RNF-02, RNF-09
- **Dependencias:** ISSUE-001, ISSUE-002

### Descripción

Crear las vistas, formularios y URLs para registrar, consultar, actualizar y
retirar los vehículos del usuario autenticado, con el modelo de ISSUE-001.

### Criterios de aceptación

- Un usuario puede registrar múltiples vehículos.
- El formulario valida los datos y muestra los errores junto al campo
  correspondiente.
- Se puede consultar el listado y el detalle de los vehículos propios.
- Se pueden actualizar los datos, incluido el kilometraje, sin alterar el
  historial existente.
- Retirar un vehículo lo marca como inactivo sin eliminar su historial.
- Un usuario no puede ver ni modificar vehículos de otro usuario.

---

## ISSUE-004 - Definir el catálogo de categorías

- **Prioridad:** Alta
- **Estado:** Pendiente
- **RF/RNF relacionados:** RF-09, RF-14, RF-16, RF-18, RF-21
- **Dependencias:** ISSUE-001

### Descripción

Cargar el catálogo de categorías predefinidas que exige RF-09 y agrupar cada
categoría en un tipo de actividad (mantenimiento, reparación, modificación u
otro gasto), para que registros, filtros, estadísticas e informes usen un único
catálogo.

### Criterios de aceptación

- El catálogo contiene todas las categorías de RF-09, incluida la de otro gasto
  relacionado.
- El catálogo queda cargado automáticamente al aplicar las migraciones.
- Cada categoría pertenece a un tipo de actividad, que permite filtrar por
  actividad y calcular el gasto en mantenimientos, reparaciones y
  modificaciones.
- Formularios, filtros, estadísticas y comparaciones obtienen las categorías
  del mismo catálogo.

---

## ISSUE-005 - Registrar gastos e intervenciones

- **Prioridad:** Alta
- **Estado:** Pendiente
- **RF/RNF relacionados:** RF-07, RF-08, RF-12, RNF-07, RNF-08
- **Dependencias:** ISSUE-003, ISSUE-004

### Descripción

Implementar el formulario, la vista y la validación de negocio para registrar
cualquier gasto o actividad de un vehículo propio, con el modelo de ISSUE-001 y
el catálogo de ISSUE-004.

### Criterios de aceptación

- Se pueden registrar mantenimientos, reparaciones, modificaciones, revisiones,
  trámites, seguros, impuestos, combustible y otros gastos.
- El formulario solicita fecha, categoría, descripción, costo y kilometraje.
- Se rechazan campos obligatorios incompletos.
- Se rechazan costos negativos, fechas inválidas y kilometrajes inválidos.
- Las validaciones se ejecutan también fuera de la interfaz.
- Los errores se muestran junto al campo sin guardar un registro inválido.
- Solo se pueden registrar gastos en vehículos propios.

---

## ISSUE-006 - Adjuntar y consultar evidencias

- **Prioridad:** Media
- **Estado:** Pendiente
- **RF/RNF relacionados:** RF-10, RF-15, RNF-02, RNF-04, RNF-16
- **Dependencias:** ISSUE-005

### Descripción

Permitir adjuntar facturas, fotografías, cotizaciones y comprobantes a un
registro, así como consultarlos posteriormente, con el modelo de evidencia de
ISSUE-001. Incluye la validación, el almacenamiento y la descarga controlada de
los archivos.

### Criterios de aceptación

- Un registro puede tener una o varias evidencias.
- Se aceptan únicamente los formatos definidos por la aplicación.
- Los archivos inválidos o incompatibles se rechazan con un mensaje claro.
- Un usuario solo puede consultar o descargar sus propios archivos.
- Los archivos almacenados no se ejecutan como contenido de la aplicación.

---

## ISSUE-007 - Editar y eliminar gastos e intervenciones

- **Prioridad:** Alta
- **Estado:** Pendiente
- **RF/RNF relacionados:** RF-11, RNF-08, RNF-09
- **Dependencias:** ISSUE-005

### Descripción

Implementar la edición y eliminación controlada de gastos e intervenciones. El
recálculo de totales tras estos cambios corresponde a ISSUE-009.

### Criterios de aceptación

- Se puede editar un registro propio conservando sus validaciones.
- La eliminación solicita confirmación.
- Un registro eliminado no aparece en consultas posteriores.
- Una operación fallida conserva el estado anterior de los datos.
- Un usuario no puede editar ni eliminar registros de otro usuario.

---

## ISSUE-008 - Consultar y filtrar el historial del vehículo

- **Prioridad:** Alta
- **Estado:** Pendiente
- **RF/RNF relacionados:** RF-13, RF-14, RF-15, RNF-02, RNF-10, RNF-13
- **Dependencias:** ISSUE-005, ISSUE-006

### Descripción

Crear la vista de historial completo por vehículo, con orden cronológico,
detalle de cada actividad y filtros de consulta. Los filtros por categoría y
tipo de actividad usan el catálogo de ISSUE-004.

### Criterios de aceptación

- El historial muestra gastos, mantenimientos, reparaciones y modificaciones.
- Los registros aparecen ordenados cronológicamente.
- Se puede filtrar por rango de fechas, categoría, actividad y vehículo.
- El detalle muestra costo, descripción, kilometraje y evidencias.
- No se muestran datos de vehículos de otros usuarios.

---

## ISSUE-009 - Implementar cálculo centralizado de totales

- **Prioridad:** Alta
- **Estado:** Pendiente
- **RF/RNF relacionados:** RF-19, RF-16, RF-17, RF-18, RF-21, RNF-06, RNF-17
- **Dependencias:** ISSUE-004, ISSUE-005, ISSUE-007

### Descripción

Crear un componente desacoplado de la interfaz para calcular totales y
agregaciones por vehículo, período y categoría.

### Criterios de aceptación

- El total corresponde exactamente a la suma de los registros válidos.
- Se pueden calcular subtotales por período y categoría.
- El cálculo se actualiza al crear, editar o eliminar registros.
- La lógica puede probarse sin depender de la interfaz.
- Los informes y estadísticas reutilizan el mismo componente.

---

## ISSUE-010 - Generar informes y estadísticas

- **Prioridad:** Media
- **Estado:** Pendiente
- **RF/RNF relacionados:** RF-16, RF-17, RNF-06, RNF-10, RNF-13
- **Dependencias:** ISSUE-008, ISSUE-009

### Descripción

Implementar el módulo de informes y estadísticas para analizar la inversión y la
evolución del gasto de cada vehículo.

### Criterios de aceptación

- Se informa el total invertido por vehículo.
- Se muestran gastos por período y por categoría.
- Se listan mantenimientos, modificaciones y costos de reparación.
- Se representa la evolución del gasto a través del tiempo.
- Los resultados coinciden con los filtros y registros seleccionados.

---

## ISSUE-011 - Comparar vehículos del usuario

- **Prioridad:** Media
- **Estado:** Pendiente
- **RF/RNF relacionados:** RF-18, RNF-06, RNF-10
- **Dependencias:** ISSUE-009, ISSUE-010

### Descripción

Agregar una vista comparativa de los vehículos pertenecientes al usuario para
identificar diferencias de costos y categorías de gasto.

### Criterios de aceptación

- Se comparan dos o más vehículos del mismo usuario.
- Se muestra el total invertido por vehículo.
- Se compara el gasto de mantenimiento y el gasto por período.
- Se identifican las principales categorías de cada vehículo.
- Los valores comparados corresponden a los registros almacenados.

---

## ISSUE-012 - Importar gastos e intervenciones

- **Prioridad:** Media
- **Estado:** Pendiente
- **RF/RNF relacionados:** RF-20, RNF-07, RNF-08, RNF-16, RNF-18
- **Dependencias:** ISSUE-004, ISSUE-005

### Descripción

Permitir cargar gastos e intervenciones desde un archivo soportado, validando
cada fila antes de incorporarla a la base de datos.

### Criterios de aceptación

- El sistema acepta únicamente el formato de archivo definido.
- Se validan fechas, importes, kilometrajes, categorías y campos obligatorios.
- Se reportan las filas aceptadas y las filas rechazadas con su motivo.
- Las filas inválidas no se guardan como registros válidos.
- El usuario puede identificar el resultado completo de la importación.

---

## ISSUE-013 - Generar reporte mensual consolidado

- **Prioridad:** Media
- **Estado:** Pendiente
- **RF/RNF relacionados:** RF-21, RF-19, RNF-06, RNF-11
- **Dependencias:** ISSUE-009

### Descripción

Crear el reporte mensual de un vehículo o del conjunto de vehículos del usuario,
con total consolidado y desglose por categoría. La medición del tiempo de
consolidación corresponde a ISSUE-014.

### Criterios de aceptación

- Se puede seleccionar el mes y el alcance del reporte.
- El reporte incluye el total consolidado.
- El reporte incluye el desglose por categoría.
- El total coincide con la suma de los registros del período.

---

## ISSUE-014 - Aplicar controles de rendimiento y escalabilidad

- **Prioridad:** Media
- **Estado:** Pendiente
- **RF/RNF relacionados:** RNF-10, RNF-11, RNF-12
- **Dependencias:** ISSUE-008, ISSUE-010, ISSUE-013

### Descripción

Optimizar consultas, cálculos e informes para mantener tiempos de respuesta
aceptables al aumentar el volumen de datos.

### Criterios de aceptación

- Consultas e informes de hasta 10.000 registros responden en un máximo de
  3 segundos, sin contar la descarga de archivos.
- El reporte mensual cumple el límite de 5 segundos.
- Las consultas utilizan índices o mecanismos equivalentes cuando corresponda.
- Las pruebas de rendimiento registran volumen de datos, entorno y resultado.

---

## ISSUE-015 - Mejorar usabilidad, accesibilidad y diseño adaptable

- **Prioridad:** Media
- **Estado:** Pendiente
- **RF/RNF relacionados:** RNF-13, RNF-14, RNF-15
- **Dependencias:** ISSUE-002, ISSUE-003, ISSUE-005, ISSUE-008, ISSUE-010

### Descripción

Aplicar criterios de usabilidad, accesibilidad y adaptación a distintos tamaños
de pantalla en los flujos principales.

### Criterios de aceptación

- Los formularios identifican campos obligatorios.
- Los mensajes de error aparecen junto al dato que debe corregirse.
- Las funciones principales se pueden operar mediante teclado.
- Los controles tienen etiquetas comprensibles y contraste suficiente.
- Registro, consulta e informes funcionan en computador, tableta y teléfono.

---

## ISSUE-016 - Completar cobertura de pruebas y trazabilidad

- **Prioridad:** Alta
- **Estado:** Pendiente
- **RF/RNF relacionados:** RNF-17, RNF-18, RNF-19, RNF-20
- **Dependencias:** ISSUE-005, ISSUE-009, ISSUE-012, ISSUE-013

### Descripción

Cada issue entrega sus propias pruebas según la definición de terminado. Este
issue revisa la cobertura del sistema completo, completa los vacíos encontrados
y construye la matriz de trazabilidad entre requisitos, código, pruebas y
criterios de aceptación.

### Criterios de aceptación

- Las validaciones de importes y fechas, el cálculo de totales, la importación
  y el reporte mensual tienen pruebas, incluidos casos inválidos y límites.
- Se documentan y cubren los vacíos de pruebas encontrados en la revisión.
- Cada RF y RNF aplicable se relaciona con una implementación y una prueba o
  criterio verificable.
- La lógica de negocio está organizada en módulos mantenibles y sin duplicación
  innecesaria.

---

## ISSUE-017 - Implementar respaldo y recuperación de datos

- **Prioridad:** Baja
- **Estado:** Pendiente
- **RF/RNF relacionados:** RNF-22
- **Dependencias:** ISSUE-001

### Descripción

Definir y automatizar un mecanismo de respaldo y recuperación que preserve los
datos y las relaciones entre usuarios, vehículos, registros y evidencias.

### Criterios de aceptación

- Se puede generar un respaldo de la información almacenada.
- Se puede restaurar el respaldo en un entorno de recuperación.
- La restauración conserva las relaciones e integridad referencial.
- Se documenta el procedimiento y el resultado de una prueba de recuperación.

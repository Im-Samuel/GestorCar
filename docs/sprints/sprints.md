# Plan de sprints de GestorCar

Plan de trabajo derivado del backlog de
[`Issues.md`](../Issues/Issues.md). Los issues se asignan una sola vez y se
ordenan respetando sus dependencias. Todos parten con estado **Pendiente**.

## Resumen

| Sprint | Objetivo | Issues |
|---|---|---:|
| Sprint 0 | Preparar el entorno de desarrollo y colaboración | 1 |
| Sprint 1 | Crear la base segura y persistente del sistema | 3 |
| Sprint 2 | Gestionar vehículos, gastos y categorías | 3 |
| Sprint 3 | Completar el historial y las evidencias | 3 |
| Sprint 4 | Entregar cálculos, informes, comparación e importación | 5 |
| Sprint 5 | Asegurar calidad, rendimiento, usabilidad y recuperación | 3 |
| **Total** |  | **18** |

---

## Sprint 0 - Entorno de desarrollo y colaboración

### Objetivo

Garantizar que todo el equipo trabaje sobre el mismo entorno, con versiones
fijadas, contenedores Docker y un flujo común con OpenSpec, antes de escribir
funcionalidad.

### Issues asignados

- **ISSUE-000:** Configurar entorno de desarrollo y colaboración.

### Entregables

- `.gitignore`, `requirements.txt` en UTF-8 y `.env.example`.
- Configuración de Django basada en variables de entorno.
- `Dockerfile` y `docker-compose.yml` con la aplicación y la base de datos.
- `README.md` con instrucciones de instalación local y con Docker.
- OpenSpec configurado para Claude Code y OpenCode.
- Convenciones de ramas, commits y pull requests.

### Criterios de cierre

- Cada integrante puede clonar el repositorio y levantar la aplicación con
  `docker compose up` o con un entorno virtual local siguiendo el `README.md`.
- El repositorio no contiene entornos virtuales, dependencias instaladas ni
  secretos.
- Existe un comando único para ejecutar las pruebas.

---

## Sprint 1 - Fundamentos de la plataforma

### Objetivo

Construir la base de usuarios y datos sobre la que se desarrollarán los demás
módulos, garantizando autenticación, persistencia e integridad referencial.

### Issues asignados

- **ISSUE-001:** Diseñar base de datos y modelos.
- **ISSUE-002:** Implementar registro y autenticación de usuarios.
- **ISSUE-003:** Implementar gestión de vehículos.

### Orden recomendado

1. ISSUE-001
2. ISSUE-002
3. ISSUE-003

### Entregables

- Modelos de usuario, vehículo, registro, categoría y evidencia, con sus
  relaciones y restricciones de integridad.
- Registro, inicio y cierre de sesión.
- Operaciones básicas de vehículos con aislamiento por usuario.

### Criterios de cierre

- Un usuario puede autenticarse y consultar únicamente sus datos.
- Puede registrar, consultar, actualizar y retirar un vehículo.
- La base de datos impide registros huérfanos.
- La información confirmada persiste después de reiniciar la aplicación.

---

## Sprint 2 - Registro de gastos y categorías

### Objetivo

Permitir registrar actividades y gastos asociados a los vehículos con
validaciones completas y categorías consistentes.

### Issues asignados

- **ISSUE-004:** Definir el catálogo de categorías.
- **ISSUE-005:** Registrar gastos e intervenciones.
- **ISSUE-007:** Editar y eliminar gastos e intervenciones.

### Orden recomendado

1. ISSUE-004
2. ISSUE-005
3. ISSUE-007

### Entregables

- Catálogo completo de categorías agrupadas por tipo de actividad.
- Formulario de gastos e intervenciones.
- Validación de fechas, importes, kilometrajes y campos obligatorios.
- Edición y eliminación con confirmación.

### Criterios de cierre

- Se pueden registrar todos los tipos de gasto definidos.
- Los datos inválidos no se guardan.
- Las categorías se reutilizan en consultas e informes.
- Editar o eliminar un registro se refleja en las consultas posteriores.

---

## Sprint 3 - Historial y evidencias

### Objetivo

Proporcionar el historial de vida del vehículo y permitir conservar los
documentos que respaldan cada actividad.

### Issues asignados

- **ISSUE-006:** Adjuntar y consultar evidencias.
- **ISSUE-008:** Consultar y filtrar el historial del vehículo.
- **ISSUE-009:** Implementar cálculo centralizado de totales.

### Orden recomendado

1. ISSUE-006
2. ISSUE-008
3. ISSUE-009

### Entregables

- Carga y consulta segura de facturas, fotografías, cotizaciones y comprobantes.
- Historial cronológico por vehículo.
- Filtros por fecha, categoría, actividad y vehículo.
- Servicio desacoplado para totales y agregaciones.

### Criterios de cierre

- El usuario puede consultar el detalle completo de una actividad y sus
  evidencias.
- El historial respeta el aislamiento entre usuarios.
- Los filtros devuelven únicamente los registros correspondientes.
- Los totales coinciden con la suma de los registros válidos.

---

## Sprint 4 - Analítica, comparación e importación

### Objetivo

Convertir los registros en información útil para la toma de decisiones y
facilitar la carga masiva y la consolidación mensual.

### Issues asignados

- **ISSUE-010:** Generar informes y estadísticas.
- **ISSUE-011:** Comparar vehículos del usuario.
- **ISSUE-012:** Importar gastos e intervenciones.
- **ISSUE-013:** Generar reporte mensual consolidado.
- **ISSUE-014:** Aplicar controles de rendimiento y escalabilidad.

### Orden recomendado

1. ISSUE-010
2. ISSUE-011
3. ISSUE-012
4. ISSUE-013
5. ISSUE-014

### Entregables

- Informes por vehículo, período y categoría.
- Estadística de evolución del gasto.
- Comparación entre vehículos del mismo usuario.
- Importación con reporte de filas aceptadas y rechazadas.
- Reporte mensual individual y consolidado.
- Mediciones de tiempo de respuesta y consolidación.

### Criterios de cierre

- Los informes y comparaciones usan el cálculo centralizado del Sprint 3.
- Las filas inválidas de una importación se reportan sin incorporarse como
  registros válidos.
- El reporte mensual muestra el total y el desglose por categoría.
- Las consultas de hasta 10.000 registros cumplen el máximo de 3 segundos.
- La consolidación mensual de hasta 10.000 registros cumple el máximo de
  5 segundos.

---

## Sprint 5 - Calidad, experiencia y recuperación

### Objetivo

Validar el sistema completo y dejarlo preparado para operación, mantenimiento,
accesibilidad y recuperación ante fallos.

### Issues asignados

- **ISSUE-015:** Mejorar usabilidad, accesibilidad y diseño adaptable.
- **ISSUE-016:** Implementar pruebas automatizadas y trazabilidad.
- **ISSUE-017:** Implementar respaldo y recuperación de datos.

### Orden recomendado

1. ISSUE-015
2. ISSUE-016
3. ISSUE-017

### Entregables

- Interfaz usable mediante teclado y adaptable a distintos dispositivos.
- Pruebas de validaciones, cálculos, importación y reportes.
- Matriz de trazabilidad entre requisitos, implementación y pruebas.
- Procedimiento probado de respaldo y recuperación.

### Criterios de cierre

- Los flujos principales muestran errores comprensibles y campos obligatorios.
- Las pruebas cubren escenarios válidos, inválidos y casos límite.
- Cada RF y RNF aplicable tiene una prueba o criterio verificable.
- Un respaldo puede restaurarse conservando las relaciones de la base de datos.
- El sistema mantiene los datos confirmados después de reinicios.

---

## Dependencias entre sprints

| Sprint | Depende de | Motivo |
|---|---|---|
| Sprint 0 | — | Prepara el entorno común del equipo. |
| Sprint 1 | Sprint 0 | Contiene la base inicial del sistema. |
| Sprint 2 | Sprint 1 | Los gastos requieren usuarios y vehículos persistentes. |
| Sprint 3 | Sprint 2 | El historial y las evidencias requieren registros de gastos. |
| Sprint 4 | Sprint 3 | Los informes requieren historial y cálculo centralizado. |
| Sprint 5 | Sprint 4 | Las pruebas finales y métricas cubren el producto completo. |

## Definición de terminado

Un issue se considerará terminado cuando:

- Sus criterios de aceptación estén cumplidos.
- La funcionalidad respete los requisitos RF/RNF relacionados.
- Se hayan agregado o actualizado las pruebas correspondientes.
- No existan errores de validación conocidos sin registrar.
- La documentación técnica o de uso relacionada esté actualizada.

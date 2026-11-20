# Backlog del Proyecto

## Plataforma de Gestión y Control de Vehículos

---

## 1. Información General

| Campo | Valor |
|---|---|
| **Nombre del proyecto** | Plataforma de Gestión y Control de Vehículos |
| **Descripción** | Sistema web para administrar vehículos, gastos, mantenimientos, modificaciones e intervenciones, con historial, informes y comparación entre vehículos. |
| **Arquitectura** | MVC (Modelo – Vista – Controlador) |
| **Stack sugerido** | Backend MVC + Base de datos relacional + Frontend adaptable |
| **Metodología** | Scrum / Desarrollo iterativo incremental |
| **Unidad de estimación** | Puntos de historia (SP) |

---

## 2. Estructura del Backlog

El backlog se organiza en **Épicas**, que agrupan **Historias de Usuario (HU)**, y cada historia se desglosa en **Tareas técnicas** alineadas a la arquitectura MVC.

| Épica | Nombre | Requerimientos asociados |
|---|---|---|
| EP-01 | Gestión de usuarios y seguridad | RF-01, RF-02, RNF-01, RNF-02, RNF-03 |
| EP-02 | Gestión de vehículos | RF-03, RF-04, RF-05, RF-06, RNF-05, RNF-09 |
| EP-03 | Registro de gastos e intervenciones | RF-07, RF-08, RF-09, RF-10, RF-11, RF-12, RNF-04, RNF-07, RNF-08 |
| EP-04 | Historial y consultas | RF-13, RF-14, RF-15 |
| EP-05 | Informes, estadísticas y comparación | RF-16, RF-17, RF-18, RF-19, RNF-06, RNF-10, RNF-11, RNF-17 |
| EP-06 | Importación y reporte mensual | RF-20, RF-21, RNF-11, RNF-16 |
| EP-07 | Calidad, pruebas y mantenibilidad | RNF-12, RNF-13, RNF-14, RNF-15, RNF-18, RNF-19, RNF-20 |
| EP-08 | Persistencia, respaldo y recuperación | RNF-21, RNF-22 |

---

## 3. Épicas e Historias de Usuario

---

### EP-01. Gestión de usuarios y seguridad

#### HU-01. Registro de usuario
**Como** persona interesada, **quiero** crear una cuenta en la plataforma, **para** administrar mis vehículos y su información asociada.

- **Prioridad:** Alta
- **Estimación:** 5 SP
- **Requerimientos:** RF-01, RNF-03

**Criterios de aceptación:**
1. El formulario solicita los datos mínimos requeridos (nombre, correo, contraseña).
2. La contraseña se almacena con hash seguro y configurable.
3. No se permite registrar dos cuentas con el mismo correo.
4. Se muestran mensajes de error junto al campo correspondiente.

**Tareas técnicas (MVC):**
- [ ] **M:** Crear modelo `Usuario` con campos y restricciones.
- [ ] **M:** Implementar hash de contraseña configurable.
- [ ] **C:** Crear controlador de registro con validaciones centralizadas.
- [ ] **V:** Diseñar formulario de registro accesible y adaptable.
- [ ] **Test:** Pruebas de validación y hash de credenciales.

---

#### HU-02. Inicio y cierre de sesión
**Como** usuario registrado, **quiero** iniciar y cerrar sesión, **para** acceder únicamente a mi información.

- **Prioridad:** Alta
- **Estimación:** 3 SP
- **Requerimientos:** RF-02, RNF-01, RNF-02

**Criterios de aceptación:**
1. El usuario puede autenticarse con credenciales válidas.
2. El sistema muestra solo la información del usuario autenticado.
3. El cierre de sesión invalida el acceso a vistas protegidas.
4. Un usuario no puede acceder a datos de otro usuario.

**Tareas técnicas (MVC):**
- [ ] **M:** Modelo de sesión y consulta de credenciales.
- [ ] **C:** Controlador de autenticación (login/logout).
- [ ] **C:** Middleware de autorización y aislamiento por usuario.
- [ ] **V:** Vistas de login y cierre de sesión.
- [ ] **Test:** Pruebas de acceso no autorizado entre usuarios.

---

### EP-02. Gestión de vehículos

#### HU-03. Registrar vehículo
**Como** usuario, **quiero** registrar uno o varios vehículos, **para** llevar su control individual.

- **Prioridad:** Alta
- **Estimación:** 5 SP
- **Requerimientos:** RF-03, RNF-05

**Criterios de aceptación:**
1. Se registran marca, modelo, año, placa, kilometraje y tipo de vehículo.
2. La placa es única por usuario.
3. El kilometraje es un valor numérico no negativo.
4. El vehículo queda asociado al usuario autenticado.

**Tareas técnicas (MVC):**
- [ ] **M:** Modelo `Vehiculo` con relaciones a `Usuario`.
- [ ] **C:** Controlador de creación con validaciones.
- [ ] **V:** Formulario de registro de vehículo.
- [ ] **Test:** Validación de campos y unicidad de placa.

---

#### HU-04. Consultar vehículos
**Como** usuario, **quiero** ver el listado y detalle de mis vehículos, **para** conocer su información.

- **Prioridad:** Alta
- **Estimación:** 3 SP
- **Requerimientos:** RF-04

**Criterios de aceptación:**
1. Se muestra el listado de vehículos del usuario autenticado.
2. Se puede acceder al detalle de cada vehículo.
3. No se muestran vehículos de otros usuarios.

**Tareas técnicas (MVC):**
- [ ] **M:** Consultas de listado y detalle por usuario.
- [ ] **C:** Controlador de consulta de vehículos.
- [ ] **V:** Vistas de listado y detalle.
- [ ] **Test:** Aislamiento de datos por usuario.

---

#### HU-05. Actualizar vehículo
**Como** usuario, **quiero** modificar los datos de un vehículo, incluido su kilometraje actual, **para** mantener la información actualizada.

- **Prioridad:** Media
- **Estimación:** 3 SP
- **Requerimientos:** RF-05, RNF-05

**Criterios de aceptación:**
1. Se pueden editar los datos del vehículo.
2. El kilometraje actual puede actualizarse.
3. Los registros históricos asociados conservan su integridad.
4. Se validan los formatos antes de guardar.

**Tareas técnicas (MVC):**
- [ ] **M:** Actualización de vehículo sin afectar historial.
- [ ] **C:** Controlador de edición con validaciones.
- [ ] **V:** Formulario de edición precargado.
- [ ] **Test:** Verificar integridad de registros históricos.

---

#### HU-06. Retirar vehículo
**Como** usuario, **quiero** marcar un vehículo como inactivo o retirado, **para** conservar su historial sin eliminarlo.

- **Prioridad:** Media
- **Estimación:** 3 SP
- **Requerimientos:** RF-06, RNF-09

**Criterios de aceptación:**
1. El vehículo se marca como inactivo/retirado.
2. El historial permanece consultable.
3. No se destruyen datos asociados.

**Tareas técnicas (MVC):**
- [ ] **M:** Campo de estado del vehículo (activo/inactivo).
- [ ] **C:** Controlador de retiro lógico.
- [ ] **V:** Acción de retiro con confirmación.
- [ ] **Test:** Verificar conservación del historial.

---

### EP-03. Registro de gastos e intervenciones

#### HU-07. Registrar gasto o intervención
**Como** usuario, **quiero** asociar a un vehículo un gasto o intervención, **para** llevar el control de lo realizado.

- **Prioridad:** Alta
- **Estimación:** 8 SP
- **Requerimientos:** RF-07, RF-08, RF-12, RNF-07, RNF-08

**Criterios de aceptación:**
1. El registro se asocia a un vehículo del usuario.
2. Incluye fecha, tipo/categoría, descripción, costo y kilometraje.
3. Se validan formato de fecha, costo no negativo y kilometraje válido.
4. No se guarda parcialmente una transacción inválida.

**Tareas técnicas (MVC):**
- [ ] **M:** Modelo `Registro` con relaciones a `Vehiculo` y `Categoria`.
- [ ] **M:** Reglas de validación de importes, fechas y kilometraje.
- [ ] **C:** Controlador de creación con validación centralizada.
- [ ] **V:** Formulario de registro con campos obligatorios indicados.
- [ ] **Test:** Pruebas de validación de importes y fechas (RNF-18).

---

#### HU-08. Categorizar registros
**Como** usuario, **quiero** seleccionar una categoría predefinida, **para** clasificar mis gastos e intervenciones.

- **Prioridad:** Alta
- **Estimación:** 3 SP
- **Requerimientos:** RF-09

**Criterios de aceptación:**
1. Existen categorías predefinidas: mantenimientos preventivos y correctivos, cambios de aceite, reparación/reemplazo de piezas, modificaciones estéticas o mecánicas, instalación de accesorios, revisiones, trámites, seguros, impuestos, combustible.
2. Existe la categoría "otro gasto relacionado".
3. La categoría es obligatoria al registrar.

**Tareas técnicas (MVC):**
- [ ] **M:** Modelo `Categoria` con carga inicial de datos.
- [ ] **C:** Controlador que expone categorías disponibles.
- [ ] **V:** Selector de categoría en formulario.
- [ ] **Test:** Verificar catálogo mínimo de categorías.

---

#### HU-09. Adjuntar evidencias y documentos
**Como** usuario, **quiero** adjuntar facturas, fotografías, cotizaciones o comprobantes a un registro, **para** respaldar la información.

- **Prioridad:** Media
- **Estimación:** 5 SP
- **Requerimientos:** RF-10, RNF-04, RNF-16

**Criterios de aceptación:**
1. Se pueden adjuntar archivos en formatos definidos.
2. Los archivos se validan antes de almacenarse.
3. Los archivos no se ejecutan como contenido de la aplicación.
4. Las evidencias pueden consultarse posteriormente.

**Tareas técnicas (MVC):**
- [ ] **M:** Modelo `Evidencia` asociado a `Registro`.
- [ ] **C:** Controlador de carga con validación de formato y tipo.
- [ ] **V:** Componente de carga y listado de evidencias.
- [ ] **Test:** Pruebas de validación y no ejecución de archivos.

---

#### HU-10. Actualizar y eliminar registros
**Como** usuario, **quiero** editar o eliminar un gasto o intervención, **para** corregir la información registrada.

- **Prioridad:** Media
- **Estimación:** 5 SP
- **Requerimientos:** RF-11, RNF-06, RNF-08

**Criterios de aceptación:**
1. Se puede editar un registro existente.
2. Se solicita confirmación antes de eliminar.
3. Los totales e informes afectados se actualizan automáticamente.
4. No se guardan transacciones inválidas.

**Tareas técnicas (MVC):**
- [ ] **M:** Actualización y eliminación con recálculo de totales.
- [ ] **C:** Controlador de edición y eliminación con confirmación.
- [ ] **V:** Formulario de edición y diálogo de confirmación.
- [ ] **Test:** Verificar actualización de totales tras cambios.

---

### EP-04. Historial y consultas

#### HU-11. Consultar historial por vehículo
**Como** usuario, **quiero** ver el historial completo y cronológico de cada vehículo, **para** conocer su evolución.

- **Prioridad:** Alta
- **Estimación:** 5 SP
- **Requerimientos:** RF-13, RF-15

**Criterios de aceptación:**
1. Se muestran gastos, mantenimientos, reparaciones y modificaciones.
2. El orden es cronológico.
3. Se puede consultar el detalle de cada actividad.
4. Se visualizan costo, kilometraje, descripción y evidencias.

**Tareas técnicas (MVC):**
- [ ] **M:** Consulta de historial ordenado cronológicamente.
- [ ] **C:** Controlador de historial y detalle.
- [ ] **V:** Vista de línea de tiempo e detalle de actividad.
- [ ] **Test:** Verificar orden y visualización de detalles.

---

#### HU-12. Filtrar historial
**Como** usuario, **quiero** filtrar el historial por rango de fechas, categoría, tipo de actividad y vehículo, **para** encontrar información específica.

- **Prioridad:** Media
- **Estimación:** 5 SP
- **Requerimientos:** RF-14

**Criterios de aceptación:**
1. Se puede filtrar por rango de fechas.
2. Se puede filtrar por categoría.
3. Se puede filtrar por tipo de actividad.
4. Se puede filtrar por vehículo.
5. Los filtros pueden combinarse.

**Tareas técnicas (MVC):**
- [ ] **M:** Consultas con criterios dinámicos.
- [ ] **C:** Controlador de filtrado.
- [ ] **V:** Panel de filtros adaptable.
- [ ] **Test:** Pruebas de combinación de filtros.

---

### EP-05. Informes, estadísticas y comparación

#### HU-13. Generar informes por vehículo
**Como** usuario, **quiero** generar informes por vehículo, **para** analizar el total invertido y los gastos por período y categoría.

- **Prioridad:** Alta
- **Estimación:** 8 SP
- **Requerimientos:** RF-16, RNF-06, RNF-10, RNF-17

**Criterios de aceptación:**
1. Se genera informe de total invertido por vehículo.
2. Se muestran gastos por período.
3. Se muestran gastos por categoría.
4. Se listan mantenimientos y modificaciones realizadas.
5. Se muestran costos de reparación.
6. Los totales coinciden con la suma de los registros filtrados.

**Tareas técnicas (MVC):**
- [ ] **M:** Servicio de cálculo desacoplado de la interfaz (RNF-17).
- [ ] **C:** Controlador de informes con parámetros de filtro.
- [ ] **V:** Vista de informe con tablas y resúmenes.
- [ ] **Test:** Pruebas de consistencia de cálculos (RNF-18).

---

#### HU-14. Analizar evolución del gasto
**Como** usuario, **quiero** ver la evolución del gasto de un vehículo en el tiempo, **para** identificar tendencias.

- **Prioridad:** Media
- **Estimación:** 5 SP
- **Requerimientos:** RF-17, RNF-06

**Criterios de aceptación:**
1. Se presenta una serie temporal de gastos.
2. Los datos provienen de registros válidos.
3. La visualización es comprensible y adaptable.

**Tareas técnicas (MVC):**
- [ ] **M:** Agregación de gastos por período.
- [ ] **C:** Controlador de evolución de gasto.
- [ ] **V:** Gráfico de evolución adaptable.
- [ ] **Test:** Verificar exactitud de la serie temporal.

---

#### HU-15. Comparar vehículos
**Como** usuario, **quiero** comparar mis vehículos por total invertido, gasto de mantenimiento, gasto por período y principales categorías, **para** identificar cuál genera mayores gastos.

- **Prioridad:** Media
- **Estimación:** 8 SP
- **Requerimientos:** RF-18, RNF-06

**Criterios de aceptación:**
1. Se comparan vehículos por total invertido.
2. Se compara gasto de mantenimiento.
3. Se compara gasto por período.
4. Se comparan principales categorías de gasto.
5. Los totales son consistentes con los registros.

**Tareas técnicas (MVC):**
- [ ] **M:** Servicio de comparación entre vehículos.
- [ ] **C:** Controlador de comparación.
- [ ] **V:** Vista comparativa con tablas y gráficos.
- [ ] **Test:** Pruebas de consistencia entre vehículos.

---

#### HU-16. Consolidar totales automáticamente
**Como** usuario, **quiero** que los totales se calculen y actualicen automáticamente, **para** confiar en la información mostrada.

- **Prioridad:** Alta
- **Estimación:** 5 SP
- **Requerimientos:** RF-19, RNF-06

**Criterios de aceptación:**
1. Los totales se calculan a partir de registros válidos.
2. Se actualizan al crear, modificar o eliminar un registro.
3. Los totales coinciden con la suma de los registros incluidos.

**Tareas técnicas (MVC):**
- [ ] **M:** Lógica de consolidación desacoplada.
- [ ] **C:** Disparadores de recálculo en operaciones CRUD.
- [ ] **V:** Visualización de totales actualizados.
- [ ] **Test:** Pruebas de recálculo tras cada operación.

---

### EP-06. Importación y reporte mensual

#### HU-17. Importar información
**Como** usuario, **quiero** importar gastos e intervenciones desde un archivo soportado, **para** cargar datos masivamente.

- **Prioridad:** Media
- **Estimación:** 8 SP
- **Requerimientos:** RF-20, RNF-16, RNF-08

**Criterios de aceptación:**
1. Se aceptan únicamente formatos definidos por el sistema.
2. Cada fila se valida antes de aceptarse.
3. Se reportan registros aceptados y errores encontrados.
4. No se guardan parcialmente transacciones inválidas.
5. Se informa cuando un archivo no es compatible.

**Tareas técnicas (MVC):**
- [ ] **M:** Modelo de importación con validación por fila.
- [ ] **C:** Controlador de importación con reporte de resultados.
- [ ] **V:** Formulario de carga y vista de resultados.
- [ ] **Test:** Pruebas de importación con archivos válidos e inválidos (RNF-18).

---

#### HU-18. Generar reporte mensual
**Como** usuario, **quiero** generar un reporte mensual de gastos de un vehículo o del conjunto, **para** conocer el total consolidado y el desglose por categoría.

- **Prioridad:** Alta
- **Estimación:** 5 SP
- **Requerimientos:** RF-21, RNF-11

**Criterios de aceptación:**
1. Se genera reporte mensual por vehículo o conjunto.
2. Incluye total consolidado.
3. Incluye desglose por categoría.
4. Se consolida en máximo 5 segundos para hasta 10.000 registros.
5. El resultado es exacto respecto de los datos almacenados.

**Tareas técnicas (MVC):**
- [ ] **M:** Agregación mensual por vehículo y categoría.
- [ ] **C:** Controlador de reporte mensual.
- [ ] **V:** Vista de reporte mensual exportable.
- [ ] **Test:** Pruebas de rendimiento y exactitud (RNF-11).

---

### EP-07. Calidad, pruebas y mantenibilidad

#### HU-19. Garantizar usabilidad y accesibilidad
**Como** usuario, **quiero** una interfaz comprensible, accesible y adaptable, **para** usar la plataforma en cualquier dispositivo.

- **Prioridad:** Media
- **Estimación:** 5 SP
- **Requerimientos:** RNF-13, RNF-14, RNF-15

**Criterios de aceptación:**
1. Los formularios indican campos obligatorios.
2. Los errores se muestran junto al dato a corregir.
3. Las funciones principales se usan con teclado.
4. Se mantiene contraste y etiquetas comprensibles.
5. La interfaz funciona en computadores, tabletas y teléfonos.

**Tareas técnicas (MVC):**
- [ ] **V:** Diseño adaptable y accesible.
- [ ] **V:** Mensajes de error contextualizados.
- [ ] **Test:** Pruebas de accesibilidad y adaptabilidad.

---

#### HU-20. Asegurar mantenibilidad y trazabilidad
**Como** equipo de desarrollo, **queremos** un código modular, trazable y probado, **para** facilitar el mantenimiento y la evolución.

- **Prioridad:** Media
- **Estimación:** 8 SP
- **Requerimientos:** RNF-17, RNF-18, RNF-19, RNF-20

**Criterios de aceptación:**
1. La lógica de cálculo está desacoplada de la interfaz.
2. Existen pruebas para validaciones, totales, importación y reportes.
3. Cada requerimiento se relaciona con su implementación y al menos una prueba.
4. El código está organizado en módulos con convenciones consistentes.
5. Un cambio en gastos o vehículos no duplica lógica de informes.

**Tareas técnicas (MVC):**
- [ ] **M/C:** Separación de capas y módulos.
- [ ] **Test:** Suite de pruebas unitarias e integración.
- [ ] **Doc:** Matriz de trazabilidad requerimiento–implementación–prueba.

---

### EP-08. Persistencia, respaldo y recuperación

#### HU-21. Garantizar persistencia
**Como** usuario, **quiero** que mis datos se conserven tras cerrar sesión o reiniciar la aplicación, **para** no perder información.

- **Prioridad:** Alta
- **Estimación:** 3 SP
- **Requerimientos:** RNF-21

**Criterios de aceptación:**
1. Los datos confirmados persisten tras cerrar sesión.
2. Los datos persisten tras reiniciar la aplicación.
3. La integridad referencial se mantiene.

**Tareas técnicas (MVC):**
- [ ] **M:** Configuración de persistencia y transacciones.
- [ ] **Test:** Pruebas de persistencia tras reinicio.

---

#### HU-22. Implementar respaldo y recuperación
**Como** administrador, **quiero** un mecanismo de respaldo y recuperación, **para** restaurar datos sin perder integridad.

- **Prioridad:** Media
- **Estimación:** 5 SP
- **Requerimientos:** RNF-22, RNF-05

**Criterios de aceptación:**
1. Existe un mecanismo de respaldo periódico.
2. La recuperación restaura datos sin perder relaciones.
3. La integridad entre usuarios, vehículos y registros se conserva.

**Tareas técnicas (MVC):**
- [ ] **M:** Estrategia de respaldo de base de datos.
- [ ] **C:** Procedimiento de restauración.
- [ ] **Test:** Pruebas de restauración con verificación de integridad.

---

## 4. Priorización del Backlog (MoSCoW)

| Prioridad | Historias |
|---|---|
| **Must have** | HU-01, HU-02, HU-03, HU-04, HU-07, HU-08, HU-11, HU-13, HU-16, HU-18, HU-21 |
| **Should have** | HU-05, HU-06, HU-09, HU-10, HU-12, HU-14, HU-15, HU-17, HU-22 |
| **Could have** | HU-19, HU-20 |
| **Won't have (esta iteración)** | — |

---

## 5. Plan de Sprints Sugerido

| Sprint | Duración | Historias | Objetivo |
|---|---|---|---|
| **Sprint 1** | 2 semanas | HU-01, HU-02 | Autenticación y aislamiento de usuarios |
| **Sprint 2** | 2 semanas | HU-03, HU-04, HU-05, HU-06 | Gestión completa de vehículos |
| **Sprint 3** | 2 semanas | HU-07, HU-08, HU-09, HU-10 | Registro de gastos, categorías y evidencias |
| **Sprint 4** | 2 semanas | HU-11, HU-12 | Historial y filtros |
| **Sprint 5** | 2 semanas | HU-13, HU-14, HU-15, HU-16 | Informes, estadísticas y comparación |
| **Sprint 6** | 2 semanas | HU-17, HU-18 | Importación y reporte mensual |
| **Sprint 7** | 2 semanas | HU-19, HU-20, HU-21, HU-22 | Calidad, persistencia y respaldo |

---

## 6. Matriz de Trazabilidad (Resumen)

| Requerimiento | Historia(s) | Prueba / Criterio verificable |
|---|---|---|
| RF-01, RF-02 | HU-01, HU-02 | Pruebas de registro, login y aislamiento |
| RF-03 – RF-06 | HU-03 – HU-06 | Pruebas CRUD de vehículos e integridad |
| RF-07 – RF-12 | HU-07 – HU-10 | Pruebas de validación, categorías y evidencias |
| RF-13 – RF-15 | HU-11, HU-12 | Pruebas de historial, detalle y filtros |
| RF-16 – RF-19 | HU-13 – HU-16 | Pruebas de informes, evolución y consolidación |
| RF-20, RF-21 | HU-17, HU-18 | Pruebas de importación y reporte mensual |
| RNF-01 – RNF-04 | HU-01, HU-02, HU-09 | Pruebas de seguridad y archivos |
| RNF-05 – RNF-09 | HU-03 – HU-10, HU-21 | Pruebas de integridad y consistencia |
| RNF-10 – RNF-12 | HU-13, HU-18 | Pruebas de rendimiento y escalabilidad |
| RNF-13 – RNF-16 | HU-19, HU-09, HU-17 | Pruebas de usabilidad, accesibilidad y compatibilidad |
| RNF-17 – RNF-20 | HU-20 | Revisión de arquitectura y suite de pruebas |
| RNF-21, RNF-22 | HU-21, HU-22 | Pruebas de persistencia y restauración |

---

## 7. Notas sobre la Arquitectura MVC

La organización del backlog respeta la separación de responsabilidades del patrón MVC:

- **Modelo (M):** entidades `Usuario`, `Vehiculo`, `Registro`, `Categoria`, `Evidencia`, reglas de validación, cálculos desacoplados y persistencia.
- **Vista (V):** formularios, listados, línea de tiempo, paneles de filtros, informes y gráficos adaptables y accesibles.
- **Controlador (C):** gestión de peticiones, autenticación, autorización, orquestación de casos de uso, validación centralizada y manejo de errores.

Esta separación facilita el cumplimiento de **RNF-17 (desacoplamiento)**, **RNF-18 (pruebas)**, **RNF-19 (trazabilidad)** y **RNF-20 (mantenibilidad)**.

---

**Fin del documento de Backlog.**
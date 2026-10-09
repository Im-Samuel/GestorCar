# Issues del proyecto GestorCar

Backlog inicial derivado de los requisitos funcionales y no funcionales del
proyecto. Los criterios de aceptación son verificables y permiten validar cada
issue durante el desarrollo.

## Convenciones

- **Prioridad:** Alta, Media o Baja.
- **Estado inicial:** Pendiente.
- **RF/RNF:** Requisitos relacionados.

---

## ISSUE-001 - Implementar registro y autenticación de usuarios

- **Prioridad:** Alta
- **Estado:** Pendiente
- **RF/RNF relacionados:** RF-01, RF-02, RNF-01, RNF-02, RNF-03

### Descripción

Crear el módulo que permita registrar usuarios, iniciar sesión y cerrar sesión.
La información de cada usuario debe mantenerse aislada de la información de
otros usuarios.

### Criterios de aceptación

- Se puede crear una cuenta con los datos obligatorios.
- Un usuario registrado puede iniciar y cerrar sesión.
- Las credenciales no se almacenan en texto plano.
- Un usuario no puede consultar ni modificar información de otra cuenta.
- Se muestran mensajes claros cuando las credenciales son inválidas o faltan
  datos obligatorios.

---

## ISSUE-002 - Crear modelo y gestión de vehículos

- **Prioridad:** Alta
- **Estado:** Pendiente
- **RF/RNF relacionados:** RF-03, RF-04, RF-05, RF-06, RNF-05, RNF-09, RNF-21
- **Dependencias:** ISSUE-001

### Descripción

Implementar el modelo de vehículo y las operaciones para registrar, consultar,
actualizar y retirar uno o varios vehículos pertenecientes a un usuario.

### Criterios de aceptación

- Un usuario puede registrar múltiples vehículos.
- El vehículo almacena marca, modelo, año, placa, kilometraje y tipo.
- Se puede consultar el listado y el detalle de los vehículos propios.
- Se pueden actualizar los datos sin alterar el historial existente.
- Retirar un vehículo lo marca como inactivo sin eliminar su historial.
- Los datos confirmados permanecen disponibles después de reiniciar la
  aplicación.

---

## ISSUE-003 - Diseñar base de datos e integridad referencial

- **Prioridad:** Alta
- **Estado:** Pendiente
- **RF/RNF relacionados:** RF-03, RF-07, RF-10, RNF-05, RNF-06

### Descripción

Diseñar e implementar las relaciones entre usuarios, vehículos, gastos,
intervenciones y evidencias, aplicando restricciones de integridad y
transacciones consistentes.

### Criterios de aceptación

- Cada vehículo pertenece a un usuario.
- Cada gasto o intervención pertenece a un vehículo válido.
- Cada evidencia pertenece a un registro válido.
- No se pueden crear registros huérfanos.
- Una operación inválida no deja datos guardados parcialmente.
- Los cambios de datos respetan las relaciones definidas.

---

## ISSUE-004 - Registrar gastos e intervenciones

- **Prioridad:** Alta
- **Estado:** Pendiente
- **RF/RNF relacionados:** RF-07, RF-08, RF-09, RF-12, RNF-06, RNF-07, RNF-08
- **Dependencias:** ISSUE-002, ISSUE-003

### Descripción

Implementar el formulario y la lógica de negocio para registrar cualquier gasto
o actividad relacionada con un vehículo.

### Criterios de aceptación

- Se pueden registrar mantenimientos, reparaciones, modificaciones, revisiones,
  trámites, seguros, impuestos, combustible y otros gastos.
- El registro incluye fecha, categoría, descripción, costo y kilometraje.
- Se rechazan campos obligatorios incompletos.
- Se rechazan costos negativos, fechas inválidas y kilometrajes inválidos.
- Las validaciones se ejecutan también fuera de la interfaz.
- Los errores se muestran sin guardar un registro inválido.

---

## ISSUE-005 - Gestionar categorías de gastos

- **Prioridad:** Media
- **Estado:** Pendiente
- **RF/RNF relacionados:** RF-09, RF-14, RF-16, RF-18, RF-21
- **Dependencias:** ISSUE-004

### Descripción

Crear el catálogo de categorías requerido y asegurar que las categorías se
utilicen de forma uniforme en registros, filtros, estadísticas e informes.

### Criterios de aceptación

- El formulario muestra las categorías definidas por el requisito RF-09.
- Cada registro queda asociado a una categoría válida.
- Los informes agrupan correctamente los registros por categoría.
- Los filtros y las comparaciones utilizan el mismo catálogo.
- Se contempla la categoría de otro gasto relacionado.

---

## ISSUE-006 - Adjuntar y consultar evidencias

- **Prioridad:** Media
- **Estado:** Pendiente
- **RF/RNF relacionados:** RF-10, RF-15, RNF-02, RNF-04, RNF-16
- **Dependencias:** ISSUE-004

### Descripción

Permitir adjuntar facturas, fotografías, cotizaciones y comprobantes a un
registro, así como consultarlos posteriormente.

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
- **RF/RNF relacionados:** RF-11, RF-19, RNF-06, RNF-08, RNF-09
- **Dependencias:** ISSUE-004

### Descripción

Implementar la edición y eliminación controlada de gastos e intervenciones,
incluyendo la actualización de cualquier total o informe relacionado.

### Criterios de aceptación

- Se puede editar un registro propio conservando sus validaciones.
- La eliminación solicita confirmación.
- Un registro eliminado no aparece en consultas ni totales posteriores.
- Los totales se recalculan después de editar o eliminar.
- Una operación fallida conserva el estado anterior de los datos.

---

## ISSUE-008 - Consultar y filtrar el historial del vehículo

- **Prioridad:** Alta
- **Estado:** Pendiente
- **RF/RNF relacionados:** RF-13, RF-14, RF-15, RNF-02, RNF-10, RNF-13
- **Dependencias:** ISSUE-004, ISSUE-006

### Descripción

Crear la vista de historial completo por vehículo, con orden cronológico,
detalle de cada actividad y filtros de consulta.

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
- **RF/RNF relacionados:** RF-21, RF-19, RNF-06, RNF-10, RNF-11
- **Dependencias:** ISSUE-009

### Descripción

Crear el reporte mensual de un vehículo o del conjunto de vehículos del usuario,
con total consolidado y desglose por categoría.

### Criterios de aceptación

- Se puede seleccionar el mes y el alcance del reporte.
- El reporte incluye el total consolidado.
- El reporte incluye el desglose por categoría.
- El total coincide con la suma de los registros del período.
- Para un usuario con hasta 10.000 registros, la consolidación finaliza en un
  máximo de 5 segundos en condiciones normales.

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
- **Dependencias:** ISSUE-002, ISSUE-004, ISSUE-008, ISSUE-010

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

## ISSUE-016 - Implementar pruebas automatizadas y trazabilidad

- **Prioridad:** Alta
- **Estado:** Pendiente
- **RF/RNF relacionados:** RNF-17, RNF-18, RNF-19, RNF-20
- **Dependencias:** ISSUE-004, ISSUE-009, ISSUE-012, ISSUE-013

### Descripción

Crear pruebas y una matriz de trazabilidad que relacionen requisitos, código,
casos de prueba y criterios de aceptación.

### Criterios de aceptación

- Existen pruebas para validación de importes y fechas.
- Existen pruebas para cálculo de totales y actualización tras cambios.
- Existen pruebas para importación y reporte mensual.
- Las pruebas cubren casos válidos, inválidos y límites relevantes.
- Cada RF y RNF aplicable se relaciona con una implementación y una prueba o
  criterio verificable.
- La lógica de negocio está organizada en módulos mantenibles y sin duplicación
  innecesaria.

---

## ISSUE-017 - Implementar respaldo y recuperación de datos

- **Prioridad:** Baja
- **Estado:** Pendiente
- **RF/RNF relacionados:** RNF-21, RNF-22
- **Dependencias:** ISSUE-003

### Descripción

Definir y automatizar un mecanismo de respaldo y recuperación que preserve los
datos y las relaciones entre usuarios, vehículos, registros y evidencias.

### Criterios de aceptación

- Se puede generar un respaldo de la información almacenada.
- Se puede restaurar el respaldo en un entorno de recuperación.
- La restauración conserva las relaciones e integridad referencial.
- Se documenta el procedimiento y el resultado de una prueba de recuperación.
- Los datos confirmados sobreviven al cierre o reinicio de la aplicación.

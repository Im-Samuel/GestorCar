# Requerimientos funcionales

Los siguientes requisitos describen las funciones que debe ofrecer la plataforma de
gestión y control de vehículos.

## Gestión de usuarios

**RF-01. Registro de usuario.** El sistema deberá permitir que una persona cree una
cuenta para administrar sus vehículos y la información asociada.

**RF-02. Acceso a la cuenta.** El sistema deberá permitir al usuario iniciar y
cerrar sesión, y deberá mostrar únicamente la información perteneciente a su
cuenta.

## Gestión de vehículos

**RF-03. Registrar vehículo.** El sistema deberá permitir registrar uno o varios
vehículos por usuario, incluyendo como mínimo marca, modelo, año, placa,
kilometraje, tipo de vehículo y las características necesarias para identificarlo.

**RF-04. Consultar vehículos.** El sistema deberá mostrar al usuario el listado de
sus vehículos y permitir consultar la información detallada de cada uno.

**RF-05. Actualizar vehículo.** El sistema deberá permitir modificar los datos de
un vehículo, incluido su kilometraje actual, conservando la integridad de los
registros históricos asociados.

**RF-06. Retirar vehículo.** El sistema deberá permitir marcar un vehículo como
inactivo o retirado, evitando que se pierda su historial de gastos e
intervenciones.

## Registro de gastos e intervenciones

**RF-07. Registrar gasto o intervención.** El sistema deberá permitir asociar a un
vehículo un registro de mantenimiento, reparación, modificación, revisión,
trámite, seguro, impuesto, combustible u otro gasto relacionado.

**RF-08. Datos del registro.** Cada registro deberá incluir fecha de la actividad,
tipo o categoría, descripción, costo e indicación del kilometraje del vehículo en
el momento de la actividad.

**RF-09. Categorías de registro.** El sistema deberá permitir seleccionar una
categoría predefinida y deberá contemplar, como mínimo, mantenimientos
preventivos y correctivos, cambios de aceite, reparación o reemplazo de piezas,
modificaciones estéticas o mecánicas, instalación de accesorios, revisiones,
trámites, seguros, impuestos y combustible. También deberá permitir la categoría
de otro gasto relacionado.

**RF-10. Evidencias y documentos.** El sistema deberá permitir adjuntar a un
registro las evidencias relacionadas, como facturas, fotografías, cotizaciones o
comprobantes, y deberá permitir consultarlas posteriormente.

**RF-11. Actualizar y eliminar registros.** El sistema deberá permitir editar o
eliminar un gasto o intervención registrado, solicitando confirmación antes de
eliminarlo y actualizando los totales e informes afectados.

**RF-12. Validar datos.** El sistema deberá validar que la fecha, el costo y el
kilometraje tengan formatos y valores válidos, que el costo no sea negativo y que
los campos obligatorios estén completos antes de guardar el registro.

## Historial y consultas

**RF-13. Consultar historial.** El sistema deberá mostrar el historial completo de
cada vehículo, incluyendo gastos, mantenimientos, reparaciones y modificaciones,
ordenado cronológicamente.

**RF-14. Filtrar historial.** El sistema deberá permitir filtrar y consultar el
historial por rango de fechas, categoría, tipo de actividad y vehículo.

**RF-15. Consultar detalle.** El sistema deberá permitir consultar el detalle de
cada actividad, su costo, kilometraje, descripción y evidencias asociadas.

## Informes, estadísticas y comparación

**RF-16. Generar informes.** El sistema deberá generar informes por vehículo
sobre el total invertido, gastos por período, gastos por categoría,
mantenimientos realizados, modificaciones efectuadas y costos de reparación.

**RF-17. Analizar evolución del gasto.** El sistema deberá presentar la evolución
del gasto de un vehículo a través del tiempo, utilizando los registros almacenados.

**RF-18. Comparar vehículos.** El sistema deberá permitir comparar los vehículos
del usuario por total invertido, gasto de mantenimiento, gasto por período y
principales categorías de gasto.

**RF-19. Consolidar totales.** El sistema deberá calcular automáticamente los
totales de gasto a partir de los registros válidos y deberá actualizar dichos
totales cuando un registro sea creado, modificado o eliminado.

**RF-20. Importar información.** El sistema deberá permitir importar gastos e
intervenciones desde un archivo soportado, validando cada fila y reportando los
registros aceptados y los errores encontrados.

**RF-21. Reporte mensual.** El sistema deberá permitir generar un reporte mensual
de los gastos de un vehículo o del conjunto de vehículos del usuario, incluyendo
el total consolidado y el desglose por categoría.
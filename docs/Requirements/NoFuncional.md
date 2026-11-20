# Requerimientos no funcionales

Los siguientes requisitos establecen condiciones de calidad, seguridad y
operación para la plataforma.

## Seguridad y privacidad

**RNF-01. Autenticación.** El sistema deberá proteger las funciones y los datos
de cada usuario mediante autenticación.

**RNF-02. Autorización y aislamiento.** Un usuario no deberá poder consultar,
modificar, eliminar ni descargar vehículos, gastos, documentos o informes de
otro usuario.

**RNF-03. Protección de credenciales.** Las contraseñas no deberán almacenarse en
texto plano; deberán protegerse mediante un mecanismo de hash seguro y
configurable.

**RNF-04. Protección de archivos.** Los documentos adjuntos deberán validarse
antes de almacenarse y no deberán poder ejecutarse directamente como contenido
de la aplicación.

## Integridad y confiabilidad

**RNF-05. Integridad referencial.** La base de datos deberá mantener relaciones
consistentes entre usuarios, vehículos, registros y evidencias, impidiendo
registros huérfanos.

**RNF-06. Consistencia de cálculos.** Los totales, estadísticas e informes deberán
calcularse a partir de los mismos datos validados y deberán coincidir con la suma
de los registros incluidos en el filtro seleccionado.

**RNF-07. Validación centralizada.** Las validaciones de importes, fechas y demás
reglas de negocio deberán ejecutarse en el servidor o capa de dominio, además de
las validaciones de la interfaz cuando existan.

**RNF-08. Manejo de errores.** El sistema deberá informar de forma clara los
errores de validación, importación y operación, sin guardar parcialmente una
transacción inválida.

**RNF-09. Disponibilidad de la información.** La eliminación o retiro de un
vehículo no deberá destruir su historial; los datos deberán permanecer
consultables según las reglas de acceso definidas.

## Rendimiento y capacidad

**RNF-10. Tiempo de respuesta.** Para consultas e informes de hasta 10.000
registros, el sistema deberá responder en un máximo de 3 segundos en condiciones
normales de operación, excluyendo el tiempo de descarga de archivos.

**RNF-11. Consolidación mensual.** Un reporte mensual deberá consolidarse en un
máximo de 5 segundos para un usuario con hasta 10.000 registros, y el resultado
deberá ser exacto respecto de los datos almacenados.

**RNF-12. Escalabilidad.** La solución deberá permitir aumentar el número de
usuarios, vehículos y registros sin requerir cambios en el modelo de datos ni
degradar de forma significativa las operaciones habituales.

## Usabilidad y compatibilidad

**RNF-13. Usabilidad.** La interfaz deberá presentar formularios y mensajes
comprensibles, indicar los campos obligatorios y mostrar los errores junto al
dato que debe corregirse.

**RNF-14. Accesibilidad.** Las funciones principales de registro, consulta y
generación de informes deberán poder utilizarse mediante teclado y deberán
mantener contraste y etiquetas comprensibles.

**RNF-15. Adaptabilidad.** La plataforma deberá funcionar correctamente en
computadores, tabletas y teléfonos mediante una interfaz adaptable.

**RNF-16. Compatibilidad de archivos.** La importación y los documentos adjuntos
deberán aceptar únicamente formatos definidos por el sistema y deberán informar
al usuario cuando un archivo no sea compatible.

## Mantenibilidad y pruebas

**RNF-17. Separación de responsabilidades.** La lógica de cálculo de totales y
estadísticas deberá estar desacoplada de la interfaz para facilitar su
reutilización y prueba.

**RNF-18. Pruebas.** El sistema deberá contar con pruebas para las validaciones
de importes y fechas, los cálculos de totales, la importación y la generación de
reportes.

**RNF-19. Trazabilidad.** Cada requerimiento deberá poder relacionarse con su
implementación y con al menos una prueba o criterio verificable.

**RNF-20. Mantenibilidad.** El código deberá organizarse en módulos y utilizar
convenciones consistentes, de manera que una modificación en gastos o vehículos
no obligue a duplicar la lógica de informes y estadísticas.

## Respaldo y recuperación

**RNF-21. Persistencia.** Los datos confirmados deberán conservarse después de
cerrar la sesión o reiniciar la aplicación.

**RNF-22. Respaldo y recuperación.** La información almacenada deberá contar con
un mecanismo de respaldo y recuperación que permita restaurar los datos sin
perder la integridad de las relaciones entre usuarios, vehículos y registros.
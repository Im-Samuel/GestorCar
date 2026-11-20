# integridad-datos Specification

## Purpose

Define las reglas de integridad que la base de datos de GestorCar garantiza
sobre usuarios, vehículos, categorías, registros y evidencias, de modo que
ninguna vista, importación o proceso pueda dejar datos inconsistentes.

## Requirements

### Requirement: Usuario identificado por correo
El sistema SHALL identificar a cada usuario por su correo electrónico, que MUST
ser único sin distinguir mayúsculas de minúsculas, y MUST guardar la contraseña
únicamente como hash.

#### Scenario: Correo repetido con distinta capitalización
- **WHEN** existe un usuario con `ana@correo.com` y se intenta crear otro con `Ana@Correo.com`
- **THEN** la base de datos rechaza el segundo usuario

#### Scenario: Contraseña almacenada
- **WHEN** se crea un usuario con una contraseña
- **THEN** el valor guardado es un hash y no contiene la contraseña en texto plano

### Requirement: Vehículo pertenece a un usuario
Cada vehículo SHALL pertenecer a exactamente un usuario existente y MUST
almacenar marca, modelo, año, placa, kilometraje, tipo y estado.

#### Scenario: Vehículo sin dueño
- **WHEN** se intenta guardar un vehículo sin usuario o con un usuario inexistente
- **THEN** la base de datos rechaza la operación

#### Scenario: Vehículo nuevo
- **WHEN** se guarda un vehículo sin indicar su estado
- **THEN** el vehículo queda en estado activo

### Requirement: Placa única por usuario
La placa de un vehículo SHALL ser única entre los vehículos de un mismo usuario,
comparándola sin espacios ni guiones y en mayúsculas.

#### Scenario: Placa repetida para el mismo usuario
- **WHEN** un usuario ya tiene un vehículo con placa `ABC123` y se guarda otro suyo con placa `abc-123`
- **THEN** la base de datos rechaza el segundo vehículo

#### Scenario: Misma placa en usuarios distintos
- **WHEN** dos usuarios distintos registran un vehículo con placa `ABC123`
- **THEN** ambos vehículos se guardan

### Requirement: Valores numéricos válidos
La base de datos SHALL rechazar kilometrajes y costos negativos, y años de
vehículo menores que 1900.

#### Scenario: Costo negativo
- **WHEN** se intenta guardar un registro con costo `-1`
- **THEN** la base de datos rechaza el registro

#### Scenario: Kilometraje negativo
- **WHEN** se intenta guardar un vehículo o un registro con kilometraje `-1`
- **THEN** la base de datos rechaza la operación

#### Scenario: Costo cero
- **WHEN** se guarda un registro con costo `0`
- **THEN** el registro se guarda

### Requirement: Registro pertenece a un vehículo y a una categoría
Cada registro de gasto o intervención SHALL pertenecer a un vehículo existente y
a una categoría existente, y MUST almacenar fecha, descripción, costo y
kilometraje.

#### Scenario: Registro huérfano
- **WHEN** se intenta guardar un registro sin vehículo o sin categoría
- **THEN** la base de datos rechaza la operación

### Requirement: Categoría con tipo de actividad
Cada categoría SHALL tener un nombre único y pertenecer a uno de los tipos de
actividad: mantenimiento, reparación, modificación u otro gasto.

#### Scenario: Categoría duplicada
- **WHEN** se intenta crear una segunda categoría con un nombre existente
- **THEN** la base de datos rechaza la operación

### Requirement: Evidencia pertenece a un registro
Cada evidencia SHALL pertenecer a un registro existente, MUST indicar su tipo
(factura, fotografía, cotización o comprobante) y MUST eliminarse junto con su
registro.

#### Scenario: Eliminar un registro con evidencias
- **WHEN** se elimina un registro que tiene evidencias
- **THEN** sus evidencias se eliminan y no queda ninguna evidencia huérfana

### Requirement: Historial protegido
La base de datos SHALL impedir eliminar un usuario que tenga vehículos, un
vehículo que tenga registros o una categoría usada por algún registro.

#### Scenario: Eliminar un vehículo con historial
- **WHEN** se intenta eliminar un vehículo que tiene registros
- **THEN** la operación se rechaza y el vehículo y sus registros se conservan

#### Scenario: Eliminar una categoría en uso
- **WHEN** se intenta eliminar una categoría usada por un registro
- **THEN** la operación se rechaza

### Requirement: Operaciones atómicas
Cada operación que modifique varios datos relacionados SHALL confirmarse por
completo o no confirmarse en absoluto.

#### Scenario: Fallo a mitad de una operación
- **WHEN** una operación crea un registro y una de sus evidencias falla al guardarse
- **THEN** no queda guardado ni el registro ni la evidencia

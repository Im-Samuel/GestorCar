# gestion-vehiculos Specification

## Purpose

Permite que cada usuario registre, consulte, actualice y retire sus vehículos,
que son la base sobre la que se registran gastos, evidencias e informes.

## Requirements

### Requirement: Registrar vehículo
El sistema SHALL permitir que el usuario registre un vehículo con marca, modelo,
año, placa, kilometraje y tipo; el vehículo MUST quedar asociado al usuario
autenticado y en estado activo.

#### Scenario: Registro válido
- **WHEN** el usuario envía el formulario con datos válidos
- **THEN** el vehículo se guarda como suyo y activo, y se muestra su detalle con un mensaje de confirmación

#### Scenario: Varios vehículos
- **WHEN** el usuario registra un segundo vehículo con otra placa
- **THEN** ambos vehículos aparecen en su listado

### Requirement: Validar datos del vehículo
El sistema SHALL rechazar un vehículo con campos obligatorios vacíos, año
anterior a 1900 o posterior al año siguiente al actual, kilometraje negativo o
placa repetida entre los vehículos del usuario, mostrando cada error junto a su
campo. La validación MUST aplicarse también fuera de los formularios.

#### Scenario: Placa repetida
- **WHEN** el usuario tiene un vehículo con placa `ABC123` y registra otro con placa `abc 123`
- **THEN** no se guarda y se muestra un error junto al campo de placa

#### Scenario: Año fuera de rango
- **WHEN** el usuario indica el año `1899` o un año dos o más años posterior al actual
- **THEN** no se guarda y se muestra un error junto al campo de año

#### Scenario: Kilometraje negativo
- **WHEN** el usuario indica un kilometraje de `-10`
- **THEN** no se guarda y se muestra un error junto al campo de kilometraje

#### Scenario: Validación fuera del formulario
- **WHEN** se valida un vehículo con año `1800` sin pasar por el formulario
- **THEN** la validación del modelo lo rechaza

### Requirement: Consultar vehículos propios
El sistema SHALL mostrar al usuario el listado de sus vehículos, con marca,
modelo, placa, año, kilometraje y estado, y permitir abrir el detalle de cada
uno.

#### Scenario: Listado con vehículos activos y retirados
- **WHEN** el usuario tiene vehículos activos y retirados
- **THEN** el listado muestra primero los activos y marca visiblemente los retirados

#### Scenario: Sin vehículos
- **WHEN** el usuario no tiene vehículos
- **THEN** el listado indica que no hay vehículos y ofrece el enlace para registrar uno

#### Scenario: Página de inicio
- **WHEN** el usuario con sesión abre la página de inicio
- **THEN** ve el listado de sus vehículos

### Requirement: Actualizar vehículo
El sistema SHALL permitir modificar los datos de un vehículo propio, incluido
su kilometraje actual, con las mismas validaciones del registro y sin alterar
los registros ya asociados al vehículo.

#### Scenario: Actualizar kilometraje
- **WHEN** el usuario cambia el kilometraje de su vehículo de `50000` a `52000`
- **THEN** el detalle muestra `52000` y los registros del vehículo siguen asociados sin cambios

#### Scenario: Formulario precargado
- **WHEN** el usuario abre la edición de un vehículo
- **THEN** el formulario muestra los datos actuales del vehículo

### Requirement: Retirar vehículo
El sistema SHALL permitir retirar un vehículo propio, previa confirmación,
cambiando su estado a retirado y conservando todo su historial. El sistema MUST
NOT ofrecer la eliminación definitiva de vehículos.

#### Scenario: Retiro confirmado
- **WHEN** el usuario confirma el retiro de un vehículo con registros
- **THEN** el vehículo queda retirado, sigue consultable y conserva todos sus registros

#### Scenario: Retiro sin confirmar
- **WHEN** el usuario abre la acción de retiro y cancela
- **THEN** el vehículo sigue activo

### Requirement: Vehículos de otros usuarios
El sistema SHALL impedir que un usuario consulte, edite o retire un vehículo de
otro usuario, respondiendo como si no existiera.

#### Scenario: Acceso a vehículo ajeno
- **WHEN** un usuario abre el detalle, la edición o el retiro de un vehículo de otro usuario
- **THEN** el sistema responde "no encontrado" y el vehículo no cambia

#### Scenario: Listado sin vehículos ajenos
- **WHEN** dos usuarios tienen vehículos registrados
- **THEN** cada uno ve en su listado únicamente los suyos

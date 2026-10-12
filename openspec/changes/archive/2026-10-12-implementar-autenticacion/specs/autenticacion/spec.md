# Spec Delta

## Purpose

Permite que cada persona cree su cuenta en GestorCar, inicie y cierre sesión, y
garantiza que solo pueda acceder a la información de su propia cuenta.

## ADDED Requirements

### Requirement: Registro de cuenta
El sistema SHALL permitir crear una cuenta con nombre, apellido, correo,
contraseña y confirmación de la contraseña, y MUST iniciar la sesión del nuevo
usuario al completar el registro.

#### Scenario: Registro exitoso
- **WHEN** una persona sin sesión envía el formulario de registro con datos válidos
- **THEN** se crea la cuenta, queda con la sesión iniciada y llega a la página de inicio

#### Scenario: Correo ya registrado
- **WHEN** una persona intenta registrarse con un correo que ya existe, aunque cambie mayúsculas y minúsculas
- **THEN** no se crea la cuenta y se muestra un error junto al campo de correo

#### Scenario: Contraseñas distintas
- **WHEN** la contraseña y su confirmación no coinciden
- **THEN** no se crea la cuenta y se muestra un error junto al campo de confirmación

#### Scenario: Contraseña débil
- **WHEN** la contraseña es demasiado corta, demasiado común, solo numérica o muy parecida a los datos personales
- **THEN** no se crea la cuenta y se muestra el motivo junto al campo de contraseña

#### Scenario: Campos obligatorios vacíos
- **WHEN** se envía el formulario sin alguno de sus campos
- **THEN** no se crea la cuenta y cada campo faltante muestra su error

### Requirement: Inicio de sesión
El sistema SHALL permitir iniciar sesión con correo y contraseña, y MUST
responder a credenciales inválidas con un mensaje que no revele cuál de los dos
datos es incorrecto.

#### Scenario: Credenciales válidas
- **WHEN** un usuario registrado ingresa su correo y contraseña correctos
- **THEN** inicia sesión y llega a la página de inicio

#### Scenario: Credenciales inválidas
- **WHEN** se ingresa un correo inexistente o una contraseña incorrecta
- **THEN** no se inicia sesión y se muestra el mismo mensaje general en ambos casos

#### Scenario: Regreso a la página solicitada
- **WHEN** un usuario sin sesión intenta abrir una página protegida y luego inicia sesión
- **THEN** llega a la página que había solicitado

### Requirement: Cierre de sesión
El sistema SHALL permitir cerrar la sesión desde cualquier página, y después de
cerrarla las páginas protegidas MUST volver a exigir inicio de sesión.

#### Scenario: Cerrar sesión
- **WHEN** un usuario con sesión pulsa "Cerrar sesión"
- **THEN** la sesión termina y llega a la página de inicio de sesión

#### Scenario: Página protegida después de salir
- **WHEN** después de cerrar sesión se abre una página protegida
- **THEN** el sistema redirige a la página de inicio de sesión

### Requirement: Acceso protegido por defecto
Toda página del sistema SHALL requerir una sesión iniciada, excepto las páginas
de registro e inicio de sesión.

#### Scenario: Página nueva sin configuración adicional
- **WHEN** una persona sin sesión solicita cualquier página que no sea registro ni inicio de sesión
- **THEN** el sistema redirige a la página de inicio de sesión

#### Scenario: Usuario con sesión abre registro o inicio de sesión
- **WHEN** un usuario con sesión abre la página de registro o de inicio de sesión
- **THEN** el sistema lo redirige a la página de inicio

### Requirement: Aislamiento entre cuentas
Las consultas de datos que pertenecen a un usuario SHALL limitarse al usuario
autenticado, y solicitar un dato de otro usuario MUST responder como si no
existiera.

#### Scenario: Dato de otra cuenta
- **WHEN** un usuario solicita por su identificador un dato que pertenece a otro usuario
- **THEN** el sistema responde con "no encontrado" sin revelar que el dato existe

### Requirement: Formularios comprensibles y accesibles
Los formularios de autenticación SHALL indicar los campos obligatorios, mostrar
cada error junto al campo que debe corregirse y en español, y MUST poder
completarse solo con el teclado en pantallas de computador, tableta y teléfono.

#### Scenario: Error asociado al campo
- **WHEN** un formulario se envía con un error en un campo
- **THEN** el mensaje aparece junto a ese campo y está asociado a él para los lectores de pantalla

#### Scenario: Uso en teléfono
- **WHEN** se abre la página de registro en una pantalla de 360 píxeles de ancho
- **THEN** el formulario se muestra completo sin desplazamiento horizontal

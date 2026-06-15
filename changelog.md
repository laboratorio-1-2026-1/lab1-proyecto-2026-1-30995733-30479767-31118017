
--------------------------------------
Cambios al 14/06/26

- Ajustes de zona horaria que reflejan correctamente la hora de Venezuela, reajustando los datos de entrada para que de ser posible en vez de ser pedida una fecha de entrada, esta sea calculada en el momento sin interacción del usuario evitando errores de ingreso.

- Implementación de archivos para que se pueda dockerizar.

- Nuevos datos de prueba para la defensa.

- Ajustes menores para el correcto funcionamiento de validaciones.

--------------------------------------
Cambios al 30/05/26

- Reestructuración del proyecto

- Se requiere de pruebas a profundidad para verificar el correcto funcionamiento de cada mensaje de validación y hacer correcciones correspondientes.

- Se logro realizar una venta con el funcionamiento correcto de monto_total, subtotal y descontar al stock de producto cuando se realizó la venta. Se añadió un PATH en venta_producto con el único propósito de cerrar la venta de un producto y así no estar añadiendo más artículos por id_venta (En proceso pasa a Completado) pero sin modificar monto y fecha (inmutables).

- Membresia permite cambiar estado del cliente manualmente, haciendo que también pierda el acceso al gimnasio. Presenta validaciones previo a cambiar de plan. Verifica que al actualizar las fechas sean coherentes fecha inicio < fecha finalizacion.

- Ticket Mantenimiento actualiza automáticamente el estado de las maquinas al crear un ticket (se probó de Operativa a En Mantenimiento con éxito), además de validar el no crear mas de un ticket para una misma maquina cuyo mantenimiento esté en curso.

- Categoria Maquina, Entrenador, Cliente, Control de Acceso, Metodo de pago, Pago Membresia funcionan bien (POST-GET-PATH) por los momentos.

- Multiples validaciones por errores de tipado o duplicados alrededor de todas las tablas (Pendiente a realizar más pruebas).

- Separación de querys dentro de services a repositories.

- *disciplina_service.py* validaciones para evitar choques si se quiere actualizar. No permite números al ingresar su nombre. Anti-Duplicados.

- REGISTRO_VENTA, VENTA_PRODUCTO, PAGO_MEMBRESIA no llevan PATH. 

- *reserva_service.py* realiza en esta la validación de solapamiento al querer actualizar.

- *sesion_service.py* además de añadir actualización path, realiza en esta la validación de solapamiento.

- *ticket_mantenimiento_service.py* actualiza el estado de la máquina tal como pide el requisito 2.9

- *maquina.py* Cualquier usuario puede ver las máquinas, solo ADMINS pueden crearlas o modificarlas.

- *maquina_service.py* Validación de estados, campos obligatorios de nombre, actualización con estado estricto.

- *maquina_schema.py* Validación de estado al hacer update.

- *maquina_models.py* descripcion_tecnica añadida.

- *dependencies.py* Modificado para verificar roles antes de modificar los routers.

- Reorganización de módulos en *main.py*.

- Creación de archivo *utils.py* que sirve como plantilla para la paginación y así ahorrarnos el colocarla en cada archivo de services, solo crear una función que llame a utils.

- *categoria_maquina_service.py* validaciones para evitar campos nulos o repeticion de categoria

- *cliente_service.py* Validación que obliga a rellenar campos de nombre, apellido, cédula. Verifica que el ID usuario exista, se asegura que solo el rol 4 sea ingresado (cliente). Por id usuario registra un único cliente, no se puede registrar la misma cedula varias veces.

- *disciplina_service.py* El nombre de la disciplina no puede estar vacío, no puede estar vacío la descripción de la disciplina, no puede haber dos disciplinas llamadas igual.

- *entrenador_service.py* Nombre, apellido y especialidad de entrenador no nulo, mensaje de error ConflictException si el ID no existe en el sistema, solo puede ingresarse el rol 3 (entrenador), si un usuario ya esta registrado como entrenador se alerta al sistema.

- *utils.py* sirve para reutilizar código común en la paginación de todos los endpoints.

- Limpieza de los endpoints, ahora todo lo relacionado a la lógica y validaciones cambio a su lugar correspondiente.

- Creación de carpeta services y creación de los 19 archivos relacionados a las 19 tablas, trasladando la lógica de negocio y validaciones previamente ya establecidas y permitiendo la implementación de nuevas. (Arrastrando también la paginación fuera de los endpoints).

- Renombramiento de carpeta CRUD a repositories (cumple su función), cambiando los nombres de los archivos *crud_archivo.py* a *archivo_repository.py* para todas las tablas, modificando todas las importaciones relacionadas, pero manteniendo la misma lógica detrás.

- Renombreamiento de los archivos de la carpeta models para agregar la terminacion *_model* que permite una navegación más clara y organizada, modificando todas las importaciones relacionadas.

- Creación de *exceptions.py* cumpliendo con la Estructura de Error Estricta exigida en la entrega de nuestro proyecto, siendo una plantilla manipulada en services que maneja errores HTTP 400 y 409.

- Cumpliendo el punto 3. Requerimientos no funcionales se cumplen 2/3 requerimientos, la **arquitectura en capas** y la **seguridad**. Se estableció los niveles de acceso para los 4 roles por defecto del gimnasio, ADMIN, FINANZAS, ENTRENADOR, CLIENTE.

- Cumpliendo el punto 2. Requerimientos no funcionales se han implementado multiples módulos, requiere de pruebas y la implementación de reglas de negocios convenientes haciendo énfasis en pagos e inventario.

- Implementación de *config.py*, *.env*, modificación a *database.py*, *security.py*, *dependencies.py*, *env.py*, *alembic.ini* para ocultar las credenciales (la contraseña utilizada en PostgreSQL).

    Siendo que ahora discretamente se llama al archivo *.env* con los datos reales en vez de modificar *alembic.ini* y *database.py* dejando el verdadero archivo fuera del repositorio.

- Adición de *.env.example*

- Adición de *middlewares.py*

- Adición de *.gitignore* con los archivos que no deben subirse en un commit.

- Modificación ligera a requeriments.txt para utilizar pip install sin problemas.

- Cambios significativos a README.md, creación de la carpeta assets con referencias visuales para las instrucciones de ejecución de código y presentación del proyecto.

- Adición de changelog.md para llevar registro de los cambios más resaltantes realizados entre commits, organizado por fechas.

--------------------------------------
Cambios al 19/05/26

- Cambio de Auth2 a Autorización Simple.
- Implementación de Paginación para todas las tablas de la BD.
- Implementación de validaciones para Reserva y Sesion en sus respectivos archivos dentro de la carpeta de routers.


- Correciones menores, implementación de registro_venta, venta_producto en crud y routers, modificaciones de control_acceso en ambas carpetas.

- Modificación del README.md

- Implementación de requeriments.txt

- Implementación de carpeta alembic y archivo *alembic.ini*

- Implementación del archivo *main.py* y *security.py*

- Creación de todos los archivos para el CRUD, con la adición de un *base.py* los demás archivos de las 19 tablas importan Class CRUDBase para su funcionamiento.

*crud_usuario.py* encripta la contraseña antes de insertarlo en PostgreSQL.

- Implementación de datos de prueba *datos_prueba.py* que permiten cargan en el proyecto roles, maquinas/categorias, productos, planes de suscripción.

- Implementación de *dependencies.py* y *database.py*

- Eliminación de archivos endpoints planteados anteriormente (implementados con otro nombre) 
*clases.py*
*maquinas.py*
*planes.py*

Implementación de los siguientes endpoints:

- *categoria_maquina.py*
- *cliente.py*

- *control_acceso.py* presenta las **validaciones**  *"Error de validación: La fecha y hora de entrada no pueden ser futuras."*

- *disciplina.py*
- *entrenador.py*


Adición de los siguientes endpoints:

- *evaluacion_biometrica.py* presenta las **validaciones** *"El peso, la altura y el porcentaje de grasa deben ser valores estrictamente positivos."*

- *maquina.py* presenta mensaje de error al no encontrar máquina.

- *membresia.py* presenta las **validaciones** *"Error de consistencia: La fecha de finalización debe ser posterior a la fecha de inicio."* valor booleano 1 a estado de membresia activo.

- *metodo_pago.py* presenta las **validaciones** *"El nombre del método de pago es obligatorio y no puede contener únicamente espacios en blanco."*,*"El método de pago ya está registrado en el sistema."*

- *pago_membresia.py* presenta las **validaciones** *"El monto del pago debe ser mayor a 0."*,*"Esta referencia de pago ya se encuentra registrada en el sistema."*

- *plan.py* presenta las **validaciones** *""El precio del plan debe ser mayor a cero."*,*"La duración del plan debe ser de al menos 1 día."*,*El precio del plan debe ser estrictamente mayor a cero.*,*"La duración del plan debe ser de al menos 1 día."*

Y mensajes de error como *Error: No se encontró ningún plan con el ID*

--------------------------------------

Cambios al 18/05/26

Creación de los primeros endpoints en la carpeta *routers*.

- *producto.py* presenta las **validaciones**  que no permiten añadir un stock negativo o cero.

- *reserva.py* presenta **validaciones** que no permiten hacer reservas en sesiones en curso, ni reservar cuando una sesión no existe.

- *rol.py* presenta **validacion**, no puede existir un rol del mismo nombre 2 veces o más.

- *sesion.py* presenta **validaciones**, la fecha de inicio debe ser anterior a la de finalización, la cantidad de cupos no puede ser negativa.

- *ticket_mantenimiento.py* cuenta con CREATE/UPDATE/GET

- *usuario.py* cuenta con CREATE/GET

- *maquina_schema.py* fue modificada, solo se pueden ingresar 3 estados "Operativa" "En Mantenimiento" "Fuera de Servicio" e implementación de actualización de datos.

- *plan_schema.py* y *ticket_mantenimiento.py* se les fue añadido la actualización de datos (Update).

--------------------------------------

Cambios al 15/05/26

- Creación de los archivos en la carpeta schemas para las 19 tablas indicadas en el MER.

--------------------------------------

Cambios al 13/05/26

- Creación de los archivos en la carpeta models para las 19 tablas indicadas en el MER.

--------------------------------------

Cambios al 09/05/26

- Creación de la estructura del proyecto.
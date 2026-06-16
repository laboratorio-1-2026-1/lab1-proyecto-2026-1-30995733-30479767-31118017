# lab1-proyecto-2026-1-30995733-30479767-31118017
Proyecto plataforma API para SmartGym por: Ricardo Pérez - Alejandro Fajardo - Angel Curé

[Ver historial de cambios](changelog.md) < - - - [ Toda Novedad - Cambio - Actualización se verá reflejado aquí ] - - -

## Integrantes 📖


![alt text](assets/Integrantes.png)


## Universidad - Profesor 🎓


![alt text](assets/Universidad-Profesor.png)


## Descripción General de SmartGym 👓

El objetivo de este proyecto es diseñar y construir una API robusta y escalable que permita la gestión operativa, financiera y administrativa de un gimnasio moderno. La solución deberá modelar un dominio que involucra control de acceso físico, gestión de inventarios, membresías, un sistema de reservas de clases con restricciones de concurrencia y seguimiento biométrico. 
La API deberá estar documentada bajo el estándar OpenAPI/Swagger y 
protegida mediante autenticación robusta por tokens.

SmartGym API es una aplicación desarrollada con FastAPI para manejar la administración de un gimnasio: usuarios, roles, autenticación, clientes, máquinas, membresías, pagos, clases, reservas, tienda y mantenimiento.

## Características principales 💡

El backend de **SmartGym** está diseñado para cubrir de manera integral las necesidades operativas de un gimnasio moderno, aplicando reglas de negocio estrictas en cada uno de sus módulos:

* 🔒 **Seguridad y Autorización (JWT):** Autenticación robusta basada en JSON Web Tokens (Bearer). Las contraseñas están protegidas mediante hashing criptográfico avanzado (Bcrypt) y el acceso está segmentado por roles (Administrador, Entrenador, Cliente).
* 👥 **Gestión de Clientes y Biometría:** Registro detallado de usuarios, integrando un historial de evaluaciones biométricas para el seguimiento físico, protegido por validaciones lógicas de datos (evitando métricas imposibles).
* 🏋️ **Inventario y Mantenimiento:** Trazabilidad completa del ciclo de vida de las máquinas del gimnasio. Incluye un sistema de Tickets de Mantenimiento para reportar fallas, cambiar estados operativos y registrar costos de reparación.
* 💳 **Suscripciones y Finanzas:** Administración de planes de membresía, catálogo de métodos de pago y un registro de ingresos con prevención antifraude (bloqueo automático de referencias bancarias duplicadas).
* 📅 **Gestión de Clases y Reservas:** Motor de programación de sesiones de entrenamiento. Cuenta con un algoritmo preventivo que bloquea el solapamiento de horarios (tanto para entrenadores como para clientes) y un control estricto de cupos máximos por clase.
* 🛒 **Punto de Venta (POS) y Stock:** Módulo de tienda para la venta de productos con validación transaccional. El sistema descuenta automáticamente el inventario y revierte la operación (Rollback) lanzando un Error 409 en caso de falta de stock.
* 🌱 **Despliegue Automatizado (Seeders):** Al iniciar la aplicación, el sistema utiliza SQLAlchemy para crear automáticamente las tablas faltantes y ejecuta scripts de poblamiento (Datos Semilla), creando al Administrador por defecto y las configuraciones base listas para producción.
* 🏗️ **Manejo de Errores Estricto:** Arquitectura limpia que captura fallas lógicas (400 Bad Request y 409 Conflict) y las formatea en respuestas JSON estandarizadas con marcas de tiempo (Timestamp) para facilitar la integración con cualquier Frontend.

## Tecnologías utilizadas 🖱️

### 🌟 Core del Backend
* **[Python 3.x](https://www.python.org/):** Lenguaje de programación principal, manejado mayoritariamente por los estudiantes estos últimos semestres de la ingeniería.
* **[FastAPI](https://fastapi.tiangolo.com/):** Framework web de alto rendimiento basado en Starlette y Pydantic. Permite la generación automática de la documentación interactiva bajo el estándar **OpenAPI / Swagger**.
* **[Uvicorn](https://www.uvicorn.org/):** Servidor web de producción basado en la especificación ASGI para gestionar peticiones concurrentes de forma eficiente.

### 🗄️ Persistencia de Datos e Infraestructura Relacional
* **[PostgreSQL](https://www.postgresql.org/):** Motor de base de datos relacional de nivel empresarial. Maneja de manera robusta y estricta el modelo entidad-relación (MER) del gimnasio, aplicando de manera óptima llaves foráneas (`ForeignKey`).
* **[SQLAlchemy (v2)](https://www.sqlalchemy.org/):** El ORM líder de Python. Utilizado para abstraer la base de datos en objetos lógicos y modelar el patrón *Repository* a través de una clase genérica abstracta (`CRUDBase`), protegiendo la aplicación de inyecciones SQL.
* **[Alembic](https://alembic.sqlalchemy.org/):** Herramienta oficial de migraciones para SQLAlchemy. Gestiona el control de versiones e historial incremental del esquema de la base de datos en archivos de código fuente Python.

### 🔒 Validación de Datos y Seguridad Avanzada
* **[Pydantic (v2)](https://docs.pydantic.dev/):** Motor de validación de datos en tiempo de ejecución. Estructura los esquemas de entrada y salida (Schemas), asegurando tipos de datos estrictos (como `EmailStr` para correos electrónicos), saneamiento de strings y control estricto sobre datos requeridos u opcionales.
* **[Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/):** Componente especializado para la lectura segura de variables de entorno locales desde el archivo `.env`.
* **[Python-Jose (Cryptography)](https://python-jose.readthedocs.io/):** Biblioteca criptográfica utilizada para la firma, codificación y decodificación matemática de los pasaportes de acceso **JSON Web Tokens (JWT)** para la autenticación sin estado (Stateless Bearer Authentication).
* **[Passlib (Bcrypt)](https://passlib.readthedocs.io/):** Motor criptográfico encargado de transformar las contraseñas planas de los usuarios en cadenas Hash irreversibles (`Bcrypt`), garantizando el cumplimiento de los estándares internacionales de ciberseguridad.

## Estructura del proyecto 📂

```text
lab1-proyecto-2026-1-30995733-30479767-31118017/
├── alembic/                        # Centro de control y scripts de migraciones de la Base de Datos
│   ├── env.py                      # Script de ejecución de Alembic (inyecta dinámicamente el .env)
│   ├── README                      # Archivo descriptivo interno de Alembic
│   └── versions/                   # Historial de versiones incrementales de la base de datos (.py)
├── app/                            # Directorio raíz del código fuente de la aplicación
│   ├── api/                        # Capa de transporte y seguridad de endpoints HTTP
│   │   ├── dependencies.py         # Inyectores de dependencia (Guardia de seguridad / Validación JWT)
│   │   └── v1/                     # Versión 1 de la API Rest
│   │       └── routers/            # Controladores / Routers HTTP (Mapeo de endpoints en Swagger)
│   ├── core/                       # Núcleo de configuraciones globales y utilidades del sistema
│   │   ├── utils.py                # Reutilización de código para la paginación (importado en todos los services)
│   │   ├── config.py               # Centro de mando (Lee el archivo .env mediante Pydantic Settings)
│   │   ├── exceptions.py           # Definición estricta de moldes de errores JSON (400, 404, 409)
│   │   ├── middlewares.py          # Interceptores globales (Medición de tiempos, logs y auditoría)
│   │   └── security.py             # Motor criptográfico (Hasheo de claves Bcrypt y firmas JWT)
│   ├── db/                         # Infraestructura de conexión y persistencia de datos
│   │   ├── database.py             # Configuración del engine de SQLAlchemy y generador de sesiones
│   │   └── datos_prueba.py         # Seeders / Poblamiento automático de datos semilla requeridos
│   ├── models/                     # Capa de Entidades ORM (Definición de tablas relacionales)
│   │   ├── __init__.py             # Fachada de exposición limpia de modelos para el ORM
│   │   └── *_model.py              # Planos de bases de datos (Ej: usuario_model.py, maquina_model.py)
│   ├── repositories/               # Capa de Acceso a Datos (Patrón Repository aislado)
│   │   ├── base.py                 # Clase genérica abstracta CRUDBase (Select, Insert, Update, Delete)
│   │   └── *_repository.py         # Llaman a CRUDBase, pero además contiene query personalizado para cada tabla (Filtros al hacer GET).
│   ├── schemas/                    # Esquemas de Pydantic (Validación estricta y tipado JSON)
│   │   ├── paginacion_schema.py    # Moldes universales para respuestas paginadas del sistema
│   │   └── *_schema.py             # Validadores de entrada/salida de datos (Ej: usuario_schema.py)
│   ├── services/                   # Capa de Servicios / Cerebro del Negocio (Casos de Uso)
│   │   ├── __init__.py             # Inicializador de paquete de lógicas de aplicación
│   │   └── *_service.py            # Lógica de Negocio.
│   └── main.py                     # Punto de entrada principal (Inicializa FastAPI y Middlewares)
├── .env                            # Bóveda secreta de credenciales locales (Excluido de Git)
├── .gitignore                      # Listado de exclusión para evitar subir secretos a GitHub
├── .env.example                    # Contiene la contraseña que permite la conexión con PostgreSQL
├── requeriments.txt                # Librerías necesarias para correr nuestro código.
├── docker-compose.yml              # Contiene información sensible que va en la dockerizacion, aquí quien descague el repositorio debe meter su clave de postgre y la secret key.
├── Dockerfile                      # Lo escencial para el funcionalmiento del docker, requirements.txt, version de python...
├── .dockerignore                   # Archivos omitidos en la dockerización.
└── alembic.ini                     # Archivo de configuración estructural básico de Alembic
```

## Requisitos previos ⏪

- Visual Studio Code: https://code.visualstudio.com/
- Python 3.10+: https://www.python.org/
- Instalar Python + VS Code: https://www.youtube.com/watch?v=-IyA_Yvs8IQ


- PostgreSQL 18: https://www.postgresql.org/
- Instalar PostgreSQL: https://www.youtube.com/watch?v=w9ax9-s2jbE&t=23s

- Base de datos creada: `smartgym_db`

> Nota: En este proyecto la URL de conexión está hardcodeada en `.env.

--------------------------------------

## Instrucciones de Preparación 🗒️

- 1. **Clonar repositorio en tu ordenador.**

Desde la misma interfaz de GitHub una vez dentro de este repositorio (la única forma de que puedas leer este README.md es estando ya adentro) seleccionas el botón [<>Code]


![alt text](assets/ClonarRepositorio.png)


Una vez dentro, cabe aclarar que existe más de una manera de traer a la computadora los archivos.

La opción "manual" sería descargar el ZIP "Download ZIP", dirigirte hacia la carpeta donde aparecen los archivos descargados por defecto y extraerlo (Windows 11 tiene la opción sin instalar nada).

Tendremos la carpeta "lab1-proyecto-2026-1-30995733-30479767-31118017-main" y adentro otra carpeta con el mismo nombre, ahora el contenido que está dentro de esta segunda carpeta, dondé están los archivos como requeriments.txt o la carpeta de apps es lo que nos interesa.

Abrimos Visual Studio Code y en la pantalla principal en la esquina superior izquierda nos dirigimos a "File" y luego "Open Folder":

![alt text](assets/VisualCarpeta.png)

Nos dirigimos a la ruta donde tenemos descargado el archivo ya extraído y nos situamos aquí:

![alt text](assets/CarpetaSeleccionada.png)


Seleccionamos la carpeta ¡Y listo! No se te olvide que ya en la interfaz de VSCode justo al abrirla te puede saltar un mensaje de si confías en los autores "Yes, I trust the autors" seleccionas esa y con eso ya estará nuestro proyecto en tu computadora. 

La otra opción más rápida requiere de la instalación obligatoria de git para funcionar.


Veamos la imagen que está al principio de las intrucciones, al presionar [<>Code] nos situamos debajo del HTTPS en el enlace que está ahí, le damos al botón justo al lado [Copy URL to clipboard] en nuestro caso: https://github.com/laboratorio-1-2026-1/lab1-proyecto-2026-1-30995733-30479767-31118017.git

Abrimos Visual Studio Code y en una pestaña en limpio nos dirigimos a los iconos a la izquierda, más específicamente al tercero que parecen ser unas ramas:


![alt text](assets/Ramas.png)


Tras darle a "Clone repository" pegamos el enlace así:

![alt text](assets/EnlaceRepo.png)

Saltará una ventana, presionamos "Open/Abrir" y ya estaría.

Instalación / Clonación: https://www.youtube.com/watch?v=lGfuztkRr4k

No está demás decir que esta manera es más delicada no solo por tener el paso extra de git, sino que cualquiera puede manipular el código con commits.

--------------------------------------

- 2. **Configuración inicial en PostgreSQL**

Para este momento se asume ya que se ha instalado la herramienta y creado una contraseña, por lo tanto lo primero que se hace es abrir el pgAdmin4

Una vez adentro desplegamos Servers->PostgreSQL 18 y nos situamos en Databases:

![alt text](assets/Databases.png)

Click derecho, create, Database. Solo rellenamos el campo Database con **smartgym_db** y presionamos **Save**.

![alt text](assets/CreacionBD.png)

**Y LISTO** con esto terminamos la creación de la base de datos y también tenemos listo nuestro proyecto en la computadora, ahora solo falta inicializarlo.

--------------------------------------


En caso de necesitar empezar de 0 otra vez situarse en postgres y con ese marcado irse a Tools, Query Tools, a la derecha saldra una pestaña para meter comandos, para borrar la BD puedes intentar con:
```bash
DROP DATABASE IF EXISTS smartgym_db WITH (FORCE);
```
*Y presionar F5.*


En caso de querer eliminar todas las tablas autogeneradas situarse en smartgym_db irse a Tools, Query Tools, a la derecha saldra una pestaña para meter comandos, para eliminar tablas
```bash
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
```
*Y presionar F5.*

--------------------------------------


## Instrucciones de ejecución ▶️

Habiendo abierto el Visual Studio Code hay 1 archivo a modificar dependiendo de tu contraseña de PostgreSQL, en la raíz de nuestro proyecto nos dirigimos a **.env.example**, cambiamos su nombre a **.env** y reemplazamos MiContraseñaPostgreSQL por nuestra verdadera contraseña en PostgreSQL, para orientarse el .env se debe ver así por dentro antes de cambiar la clave:
:
```bash
SECRET_KEY="CLAVE_SECRETA"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL="postgresql://postgres:MiContraseñaPostgreSQL@localhost:5432/smartgym_db?client_encoding=utf8"
```

Una vez abierto Visual Studio Code y abierto la carpeta descargada en el paso i, en la raíz de nuestro proyecto, nos vamos a las opciones que hay arriba, más en específico a Terminal->New Terminal. 


![alt text](assets/Terminal.png)

Colocamos los siguientes comandos

```bash
python -m venv .venv
## En caso de que venv de error colocar este comando antes de venv, ha ocurrido también que se debe ejecutar 2 veces el primer comando para que funcione.
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Para entrar en nuestro entorno de desarrollo solo faltaría poner
```bash
.venv\Scripts\activate
```
Antes de seguir asegurate que al meter el comando anterior la terminal cambiara a verse así a la izquierda:
![alt text](assets/venv-verde.png)

De ser así instalamos todas las librerías a utilizar con el siguiente pip install:

```bash
pip install -r requeriments.txt
```

Y por último si todo salió bien ejecutamos:

```bash
python -m uvicorn app.main:app --reload
```

Al hacerlo nos debe salir unos mensajes INFO en verde de esta forma:

![alt text](assets/ExitoCodigo.png)

**FINALMENTE** Abrimos nuestro navegador de preferencia y ingresamos esta dirección:

http://127.0.0.1:8000/docs

Eso sería todo.

--------------------------------------

## DOCKER 🐳

Instalar Docker Desktop

Desde la Microsoft Store: https://apps.microsoft.com/detail/XP8CBJ40XLBWKX?hl=es-VE&gl=VE&ocid=pdpshare

Desde la web: https://docs.docker.com/desktop/setup/install/windows-install/

Asegurarse que desde la BIOS se permita ejecutar maquinas virtuales para evitar errores.

Una vez ejecutado el programa docker de fondo, asegurarse de que en docker-compose.yml esten las credenciales correspondientes en SECRET_KEY, DATABASE_URL y POSTGRES_PASSWORD de creer necesario.

En VSCode tener instalado Container Tools: https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-containers

Se debe de ejecutar en la terminal docker compose up --build (o docker-compose up --build) y así se ejecutaría el docker.

Verificar en http://localhost:8000/docs#/

Cerrar docker con Ctrl+C y luego docker compose down.


## Datos de prueba 🌱

Al iniciar la aplicación, si la base de datos está vacía, se crean datos de prueba en `app/db/datos_prueba.py`:

- Roles: Administración, Finanzas, Entrenador, Cliente
- Usuario admin: `admin@smartgym.com` / `123456789`
- `Categorías de máquinas`, `Máquinas`, `Planes de suscripción`, `Productos`, `Clientes`, `Entrenadores`

--------------------------------------
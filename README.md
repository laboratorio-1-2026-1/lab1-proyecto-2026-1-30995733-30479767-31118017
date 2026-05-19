# lab1-proyecto-2026-1-30995733-30479767-31118017
Proyecto plataforma API para SmartGym por: Ricardo Pérez - Alejandro Fajardo - Angel Curé

## Descripción
SmartGym API es una aplicación desarrollada con FastAPI para manejar la administración de un gimnasio: usuarios, roles, autenticación, clientes, máquinas, membresías, pagos, clases, reservas, tienda y mantenimiento.

## Características principales

- Autenticación con JWT
- Gestión de usuarios y roles
- Registro de clientes y evaluaciones biométricas
- Inventario de máquinas y tickets de mantenimiento
- Gestión de planes de suscripción, métodos de pago y pagos de membresía
- Reservas de clases y gestión de sesiones
- Tienda de productos
- Creación automática de tablas y datos semilla al iniciar la aplicación

## Tecnologías utilizadas

Dentro de "requirements.txt" se encuentran las librerias utilizadas para el desarrollo de la api

## Estructura del proyecto

- `app/main.py` - Entrada principal de la aplicación y registro de routers
- `app/api/v1/routers/` - Rutas de la API
- `app/models/` - Modelos ORM de SQLAlchemy
- `app/schemas/` - Esquemas de Pydantic usados para validación
- `app/db/database.py` - Conexión a la base de datos y sesión de SQLAlchemy
- `app/db/datos_prueba.py` - Datos de prueba para inicializar roles, usuario admin, máquinas, planes y productos
- `app/core/security.py` - Gestión de JWT y hash de contraseñas
- `alembic/` - Migraciones de base de datos
- `alembic.ini` - Configuración de Alembic y URL de PostgreSQL

## Requisitos previos

- Python 3.10+ instalado
- PostgreSQL instalado y en ejecución
- Base de datos creada: `smartgym_db`

> Nota: En este proyecto la URL de conexión está hardcodeada en `app/db/database.py` y `alembic.ini`.

## Configuración de la base de datos

La conexión actual está configurada como:

- `postgresql://postgres:M070526@localhost:5432/smartgym_db?client_encoding=utf8`

Asegúrate de crear la base de datos `smartgym_db` en PostgreSQL y que tu contraseña de coincida con la contraseña 
en los archivos del proyecto en alembic.ini linea 89.

## Instalación

Desde la raíz del proyecto:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install "fastapi[standard]" sqlalchemy alembic psycopg2-binary passlib bcrypt==4.0.1 "python-jose[cryptography]" python-multipart pg8000
```

## Ejecución

Inicia la API con:

```bash
python -m uvicorn app.main:app --reload
```

La aplicación iniciará en `http://127.0.0.1:8000`.

## Documentación interactiva

- Swagger UI: `http://127.0.0.1:8000/docs`

## Datos de prueba

Al iniciar la aplicación, si la base de datos está vacía, se crean datos de prueba en `app/db/datos_prueba.py`:

- Roles: Administración, Finanzas, Entrenador, Cliente
- Usuario admin: `admin@smartgym.com` / `1234`
- Categorías de máquinas
- Máquinas de ejemplo
- Planes de suscripción
- Productos de la tienda
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import engine, Base, SessionLocal
from app.db.datos_prueba import poblar_datos_semilla


from app.api.v1.routers import (
    usuario, 
    rol, 
    auth,
    categoria_maquina, 
    ticket_mantenimiento, 
    maquina, 
    metodo_pago,
    plan, 
    pago_membresia,
    membresia,
    control_acceso,
    disciplina, 
    sesion,
    cliente,  
    evaluacion_biometrica,
    entrenador,
    reserva,
    producto,

)

Base.metadata.create_all(bind=engine)

def inicializar_datos():
    db = SessionLocal()
    try:
        poblar_datos_semilla(db)
    finally:
        db.close()
inicializar_datos()

app = FastAPI(
    title="SmartGym API",
    description="API para la gestión integral de gimnasios - UCLA Laboratorio I",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Inicio"])
def read_root():
    return {
        "message": "Bienvenido a la API de SmartGym",
        "status": "Operativa",
        "universidad": "UCLA",
        "profesor": "Jonathan Falcon"
    }


# Módulo de Seguridad
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Seguridad"])
app.include_router(rol.router, prefix="/api/v1/roles", tags=["Seguridad"])
app.include_router(usuario.router, prefix="/api/v1/usuarios", tags=["Seguridad"])

# Módulo de Gestión de Clientes y Evaluaciones Biométricas
app.include_router(cliente.router, prefix="/clientes", tags=["Clientes y Evaluaciones"])
app.include_router(evaluacion_biometrica.router, prefix="/evaluaciones-biometricas", tags=["Cliente y Evaluaciones"])

# Módulo de Inventario y Mantenimiento
app.include_router(categoria_maquina.router, prefix="/api/v1/categorias", tags=["Inventario de Maquinas"])
app.include_router(maquina.router, prefix="/api/v1/maquinas", tags=["Inventario"])
app.include_router(ticket_mantenimiento.router, prefix="/api/v1/tickets", tags=["Inventario de Maquinas"])

# Módulo de Suscripciones
app.include_router(metodo_pago.router, prefix="/api/v1/metodos-pago", tags=["Suscripciones y Pagos"])
app.include_router(plan.router, prefix="/api/v1/planes", tags=["Suscripciones y Pagos"])
app.include_router(pago_membresia.router, prefix="/api/v1/pagos-membresia", tags=["Suscripciones y Pagos"])
app.include_router(membresia.router, prefix="/api/v1/membresias", tags=["Suscripciones y Pagos"])
app.include_router(control_acceso.router, prefix="/api/v1/control-acceso", tags=["Control de Acceso"]) 

# Módulo de Tienda
app.include_router(producto.router, prefix="/api/v1/productos", tags=["Tienda y Ventas"])

# Módulo de Gestión de Clases y Reservas
app.include_router(entrenador.router, prefix="/api/v1/entrenadores", tags=["Gestión de Clases"])
app.include_router(disciplina.router, prefix="/api/v1/disciplinas", tags=["Gestión de Clases"])
app.include_router(sesion.router, prefix="/api/v1/sesiones", tags=["Gestión de Clases"])
app.include_router(reserva.router, prefix="/api/v1/reservas", tags=["Gestión de Clases"])

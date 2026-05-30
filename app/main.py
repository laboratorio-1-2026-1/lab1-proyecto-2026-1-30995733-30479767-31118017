from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.core.exceptions import SmartGymException
from app.db.database import engine, Base, SessionLocal
from app.db.datos_prueba import poblar_datos_semilla
from app.core.middlewares import GlobalMiddleware
from app.api.v1.api_router import api_router

Base.metadata.create_all(bind=engine)

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

app.add_middleware(GlobalMiddleware)

@app.exception_handler(SmartGymException)
async def smartgym_exception_handler(request: Request, exc: SmartGymException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.error_type,
            "codigoInterno": exc.codigo_interno,
            "mensaje": exc.mensaje,
            "timestamp": exc.timestamp
        }
    )

@app.get("/", tags=["Inicio"])
def read_root():
    return {
        "message": "Bienvenido a la API de SmartGym",
        "status": "Operativa",
        "universidad": "UCLA",
        "profesor": "Jonathan Falcon"
    }

app.include_router(api_router, prefix="/api/v1")

def inicializar_datos():
    db = SessionLocal()
    try:
        poblar_datos_semilla(db)
    finally:
        db.close()

inicializar_datos()
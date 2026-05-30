from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.schemas import evaluacion_biometrica_schema
from app.db.database import get_db
from app.services import evaluacion_biometrica_service
from app.api.dependencies import VerificarRol, ADMIN, ENTRENADOR, CLIENTE

router = APIRouter()

@router.post("/", response_model=evaluacion_biometrica_schema.EvaluacionBiometricaResponse, summary="Crear evaluación biometrica", dependencies=[Depends(VerificarRol([ADMIN, ENTRENADOR]))])
def create_evaluacion(*, db: Session = Depends(get_db), eval_in: evaluacion_biometrica_schema.EvaluacionBiometricaCreate):
    return evaluacion_biometrica_service.crear_evaluacion(db=db, eval_in=eval_in)

@router.get("/", response_model=evaluacion_biometrica_schema.EvaluacionBiometricaPaginatedResponse, summary="Obtener evaluaciones biometricas", dependencies=[Depends(VerificarRol([ADMIN, ENTRENADOR, CLIENTE]))])
def read_evaluaciones(
    id_cliente: Optional[int] = Query(None, description="Filtrar historial por un ID de cliente específico"), 
    orden_fecha: str = Query("desc", enum=["asc", "desc"], description="Ordenar de forma cronológica: desc (más reciente primero) o asc (histórico)"),
    page: int = Query(1, ge=1, description="Número de página"), 
    page_size: int = Query(10, ge=1, description="Tamaño de la página"),
    db: Session = Depends(get_db)
):
    return evaluacion_biometrica_service.obtener_evaluaciones_paginadas(
        db=db, 
        page=page, 
        page_size=page_size, 
        id_cliente=id_cliente, 
        orden_fecha=orden_fecha
    )

@router.patch("/{id_evaluacion}", response_model=evaluacion_biometrica_schema.EvaluacionBiometricaResponse, summary="Actualizar evaluación biometrica", dependencies=[Depends(VerificarRol([ADMIN, ENTRENADOR]))])
def update_evaluacion(*, db: Session = Depends(get_db), id_evaluacion: int, eval_in: evaluacion_biometrica_schema.EvaluacionBiometricaUpdate):
    return evaluacion_biometrica_service.actualizar_evaluacion(db=db, id_evaluacion=id_evaluacion, eval_in=eval_in)
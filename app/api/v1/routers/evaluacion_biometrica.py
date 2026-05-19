from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import math
from app.schemas import evaluacion_biometrica_schema
from app.crud.crud_evaluacion import evaluacion as crud_evaluacion
from app.db.database import get_db

router = APIRouter()

@router.post("/", response_model=evaluacion_biometrica_schema.EvaluacionBiometricaResponse)
def create_evaluacion(
    *,
    db: Session = Depends(get_db),
    eval_in: evaluacion_biometrica_schema.EvaluacionBiometricaCreate
):
    if eval_in.peso <= 0 or eval_in.altura <= 0 or eval_in.porc_grasa <= 0:
        raise HTTPException(status_code=400, detail="Error de validación: El peso, la altura y el porcentaje de grasa deben ser positivos.")
        
    nueva_evaluacion = crud_evaluacion.create(db, obj_in=eval_in.model_dump())
    return nueva_evaluacion

@router.get("/", response_model=evaluacion_biometrica_schema.EvaluacionBiometricaPaginatedResponse)
def read_evaluaciones(db: Session = Depends(get_db), page: int = 1, page_size: int = 10):
    if page < 1 or page_size < 1:
        raise HTTPException(status_code=400, detail="Los parámetros de página deben ser mayores a 0.")
    
    total_rows = db.query(crud_evaluacion.model).count()
    total_pages = math.ceil(total_rows / page_size) if total_rows > 0 else 1
    
    skip = (page - 1) * page_size
    evaluaciones = crud_evaluacion.get_multi(db, skip=skip, limit=page_size)
    
    return {
        "meta": {"total_rows": total_rows, "current_page": page, "page_size": page_size, "total_pages": total_pages},
        "rows": evaluaciones
    }
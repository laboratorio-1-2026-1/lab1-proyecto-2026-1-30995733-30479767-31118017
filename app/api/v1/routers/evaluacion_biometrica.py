from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
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
        raise HTTPException(
            status_code=400,
            detail="Error de validación: El peso, la altura y el porcentaje de grasa deben ser valores estrictamente positivos."
        )
        
    nueva_evaluacion = crud_evaluacion.create(db, obj_in=eval_in.model_dump())
    return nueva_evaluacion

@router.get("/", response_model=List[evaluacion_biometrica_schema.EvaluacionBiometricaResponse])
def read_evaluaciones(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    evaluaciones = crud_evaluacion.get_multi(db, skip=skip, limit=limit)
    return evaluaciones
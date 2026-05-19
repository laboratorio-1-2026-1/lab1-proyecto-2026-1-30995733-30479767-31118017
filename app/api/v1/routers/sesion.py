from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas import sesion_clase_schema
from app.crud.crud_sesion import sesion as crud_sesion
from app.db.database import get_db 

router = APIRouter()

@router.post("/", response_model=sesion_clase_schema.SesionClaseResponse)
def create_sesion(
    *,
    db: Session = Depends(get_db),
    sesion_in: sesion_clase_schema.SesionClaseCreate
):
    """
    Programa una nueva sesión de clase en un horario específico.
    """
    if sesion_in.fecha_inic >= sesion_in.fecha_fin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La fecha de inicio debe ser anterior a la fecha de finalización."
        )
    if sesion_in.cupos < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El número de cupos asignados a la sesión no puede ser negativo."
        )

    nueva_sesion = crud_sesion.create(db, obj_in=sesion_in.model_dump())
    return nueva_sesion

@router.get("/", response_model=List[sesion_clase_schema.SesionClaseResponse])
def read_sesiones(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Lista todas las sesiones de clases programadas.
    """
    sesiones = crud_sesion.get_multi(db, skip=skip, limit=limit)
    return sesiones
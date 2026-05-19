from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.schemas.control_acceso_schema import ControlAccesoCreate, ControlAccesoResponse
from app.crud.crud_control_acceso import control_acceso as crud_control_acceso
from app.db.database import get_db

router = APIRouter()

@router.post("/", response_model=ControlAccesoResponse, status_code=status.HTTP_201_CREATED)
def create_acceso(
    *,
    db: Session = Depends(get_db),
    acceso_in: ControlAccesoCreate
):
    if acceso_in.fecha_entrada > datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error de validación: La fecha y hora de entrada no pueden ser futuras."
        )
    
    nuevo_acceso = crud_control_acceso.create(db, obj_in=acceso_in.model_dump())
    return nuevo_acceso

@router.get("/", response_model=List[ControlAccesoResponse])
def read_accesos(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    accesos = crud_control_acceso.get_multi(db, skip=skip, limit=limit)
    return accesos
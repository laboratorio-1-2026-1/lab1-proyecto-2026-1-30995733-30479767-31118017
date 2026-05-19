from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.schemas import reserva_schema
from app.crud.crud_reserva import reserva as crud_reserva
from app.crud.crud_sesion import sesion as crud_sesion
from app.db.database import get_db
from app.api.dependencies import get_current_user 
from app.models.usuario import Usuario


router = APIRouter()

@router.post("/", response_model=reserva_schema.ReservaResponse)
def create_reserva(
    *,
    db: Session = Depends(get_db),
    reserva_in: reserva_schema.ReservaCreate,
    current_user: Usuario = Depends(get_current_user)
):

    sesion_existente = crud_sesion.get(db, id=reserva_in.id_sesion)
    
    if not sesion_existente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La sesión de clase solicitada no existe."
        )
    
    if datetime.now() >= sesion_existente.fecha_inic:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pueden realizar reservas para una sesión que ya está en curso o ha finalizado."
        )
    
    nueva_reserva = crud_reserva.create(db, obj_in=reserva_in.model_dump())
    return nueva_reserva

@router.get("/", response_model=List[reserva_schema.ReservaResponse])
def read_reservas(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    reservas = crud_reserva.get_multi(db, skip=skip, limit=limit)
    return reservas


@router.delete("/{id_reserva}", response_model=reserva_schema.ReservaResponse)
def delete_reserva(
    *,
    db: Session = Depends(get_db),
    id_reserva: int,
    current_user: Usuario = Depends(get_current_user)
):
    reserva_actual = crud_reserva.get(db=db, id=id_reserva)
    if not reserva_actual:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Error: Reserva no encontrada."
        )
    reserva_eliminada = crud_reserva.remove(db=db, id=id_reserva)
    
    return reserva_eliminada
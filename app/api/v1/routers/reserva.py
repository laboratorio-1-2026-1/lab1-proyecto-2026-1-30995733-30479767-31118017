from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import math
from typing import List
from datetime import datetime
from app.schemas import reserva_schema
from app.crud.crud_reserva import reserva as crud_reserva
from app.crud.crud_sesion import sesion as crud_sesion
from app.models.reserva import Reserva
from app.models.sesion_clase import SesionClase 
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


# Validaciones que evitan choques de horarios, datos incorrectos y reservas para sesiones ya iniciadas o finalizadas
    sesion_destino = crud_sesion.get(db, id=reserva_in.id_sesion)
    if not sesion_destino:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La sesión de clase solicitada no existe."
        )
    if datetime.now() >= sesion_destino.fecha_inic:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pueden realizar reservas para una sesión que ya está en curso o ha finalizado."
        )

    reserva_chocante = db.query(Reserva).join(SesionClase, Reserva.id_sesion == SesionClase.id_sesion).filter(
        Reserva.id_cliente == reserva_in.id_cliente,
        sesion_destino.fecha_inic < SesionClase.fecha_fin,
        sesion_destino.fecha_fin > SesionClase.fecha_inic
    ).first()

    if reserva_chocante:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Conflicto de reservas: El cliente ya tiene una reserva activa para otra disciplina en este mismo horario."
        )
    nueva_reserva = crud_reserva.create(db, obj_in=reserva_in.model_dump())
    return nueva_reserva

@router.get("/", response_model=reserva_schema.ReservaPaginatedResponse)
def read_reservas(db: Session = Depends(get_db), page: int = 1, page_size: int = 10):
    if page < 1 or page_size < 1:
        raise HTTPException(status_code=400, detail="Los parámetros de página deben ser mayores a 0.")
    
    total_rows = db.query(crud_reserva.model).count()
    total_pages = math.ceil(total_rows / page_size) if total_rows > 0 else 1
    
    skip = (page - 1) * page_size
    reservas = crud_reserva.get_multi(db, skip=skip, limit=page_size)
    
    return {
        "meta": {"total_rows": total_rows, "current_page": page, "page_size": page_size, "total_pages": total_pages},
        "rows": reservas
    }

@router.delete("/{id_reserva}", response_model=reserva_schema.ReservaResponse)
def delete_reserva(
    *,
    db: Session = Depends(get_db),
    id_reserva: int,
    current_user: Usuario = Depends(get_current_user)
):
    reserva_actual = crud_reserva.get(db=db, id=id_reserva)
    if not reserva_actual:
        raise HTTPException(status_code=404, detail="Error: Reserva no encontrada")
    return crud_reserva.remove(db=db, id=id_reserva)
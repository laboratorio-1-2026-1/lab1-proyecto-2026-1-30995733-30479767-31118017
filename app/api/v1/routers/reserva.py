from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from app.schemas import reserva_schema
from app.db.database import get_db
from app.services import reserva_service 
from app.api.dependencies import VerificarRol, ADMIN, CLIENTE, ENTRENADOR

router = APIRouter()

@router.post("/", response_model=reserva_schema.ReservaResponse, summary="Crear reserva", dependencies=[Depends(VerificarRol([ADMIN, CLIENTE]))])
def create_reserva(*, db: Session = Depends(get_db), reserva_in: reserva_schema.ReservaCreate):
    return reserva_service.crear_reserva(db=db, reserva_in=reserva_in)

@router.get("/", response_model=reserva_schema.ReservaPaginatedResponse, summary="Obtener reservas", dependencies=[Depends(VerificarRol([ADMIN, ENTRENADOR, CLIENTE]))])
def read_reservas(
    id_cliente: Optional[int] = None, 
    id_sesion: Optional[int] = None,  
    page: int = 1, 
    page_size: int = 10,
    db: Session = Depends(get_db)
):
    return reserva_service.obtener_reservas_paginadas(db=db, page=page, page_size=page_size, id_cliente=id_cliente, id_sesion=id_sesion)

@router.patch("/{id_reserva}", response_model=reserva_schema.ReservaResponse, summary="Actualizar reserva", dependencies=[Depends(VerificarRol([ADMIN, CLIENTE]))])
def update_reserva(*, db: Session = Depends(get_db), id_reserva: int, reserva_in: reserva_schema.ReservaUpdate):
    return reserva_service.actualizar_reserva(db=db, id_reserva=id_reserva, reserva_in=reserva_in)
from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_current_user 
from app.models.usuario import Usuario

from app.schemas import ticket_mantenimiento_schema
from app.crud.crud_ticket_mantenimiento import ticket_mantenimiento as crud_ticket_mantenimiento
from app.db.database import get_db 

router = APIRouter()

@router.post("/", response_model=ticket_mantenimiento_schema.TicketMantenimientoResponse)
def create_ticket(
    *,
    db: Session = Depends(get_db),
    ticket_in: ticket_mantenimiento_schema.TicketMantenimientoCreate,
    current_user: Usuario = Depends(get_current_user)
):

    nuevo_ticket = crud_ticket_mantenimiento.create(db, obj_in=ticket_in.model_dump())
    return nuevo_ticket


@router.patch("/{id_ticket}", response_model=ticket_mantenimiento_schema.TicketMantenimientoResponse)
def update_ticket_status(
    *,
    db: Session = Depends(get_db),
    id_ticket: int,
    ticket_in: ticket_mantenimiento_schema.TicketMantenimientoUpdate,
    current_user: Usuario = Depends(get_current_user)
):

    ticket_actual = crud_ticket_mantenimiento.get(db=db, id=id_ticket)
    if not ticket_actual:
        raise HTTPException(status_code=404, detail="Error: Ticket de mantenimiento no encontrado")

    ticket_actualizado = crud_ticket_mantenimiento.update(
        db=db, 
        db_obj=ticket_actual, 
        obj_in=ticket_in
    )
    
    return ticket_actualizado


@router.get("/", response_model=List[ticket_mantenimiento_schema.TicketMantenimientoResponse])
def read_tickets(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    tickets = crud_ticket_mantenimiento.get_multi(db, skip=skip, limit=limit)
    return tickets
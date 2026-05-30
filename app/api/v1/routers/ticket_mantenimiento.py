from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.schemas import ticket_mantenimiento_schema
from app.db.database import get_db 
from app.services import ticket_mantenimiento_service
from app.api.dependencies import VerificarRol, ADMIN, ENTRENADOR

router = APIRouter()

@router.post("/", response_model=ticket_mantenimiento_schema.TicketMantenimientoResponse, summary="Crear ticket de mantenimiento", dependencies=[Depends(VerificarRol([ADMIN, ENTRENADOR]))])
def create_ticket(*, db: Session = Depends(get_db), ticket_in: ticket_mantenimiento_schema.TicketMantenimientoCreate):
    return ticket_mantenimiento_service.crear_ticket(db=db, ticket_in=ticket_in)

@router.get("/", response_model=ticket_mantenimiento_schema.TicketMantenimientoPaginatedResponse, summary="Obtener tickets de mantenimiento", dependencies=[Depends(VerificarRol([ADMIN, ENTRENADOR]))])
def read_tickets(
    id_maquina: Optional[int] = Query(None, description="Filtrar el historial completo de reparaciones por ID de máquina"), 
    page: int = Query(1, ge=1), 
    page_size: int = Query(10, ge=1),
    db: Session = Depends(get_db)
):
    return ticket_mantenimiento_service.obtener_tickets_paginados(db=db, page=page, page_size=page_size, id_maquina=id_maquina)

@router.patch("/{id_ticket}", response_model=ticket_mantenimiento_schema.TicketMantenimientoResponse, summary="Actualizar ticket de mantenimiento", dependencies=[Depends(VerificarRol([ADMIN]))])
def update_ticket(*, db: Session = Depends(get_db), id_ticket: int, ticket_in: ticket_mantenimiento_schema.TicketMantenimientoUpdate):
    return ticket_mantenimiento_service.actualizar_estado_ticket(db=db, id_ticket=id_ticket, ticket_in=ticket_in)
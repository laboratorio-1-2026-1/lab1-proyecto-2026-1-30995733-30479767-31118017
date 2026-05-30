from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.schemas import membresia_schema
from app.db.database import get_db 
from app.services import membresia_service
from app.api.dependencies import VerificarRol, ADMIN, FINANZAS, CLIENTE, ENTRENADOR

router = APIRouter()

@router.post("/", response_model=membresia_schema.MembresiaResponse, summary="Crear membresía", status_code=status.HTTP_201_CREATED, dependencies=[Depends(VerificarRol([ADMIN, FINANZAS]))])
def create_membresia(*, db: Session = Depends(get_db), membresia_in: membresia_schema.MembresiaCreate):
    return membresia_service.crear_membresia(db=db, membresia_in=membresia_in)

@router.get("/", response_model=membresia_schema.MembresiaPaginatedResponse, summary="Obtener membresías", dependencies=[Depends(VerificarRol([ADMIN, FINANZAS, ENTRENADOR, CLIENTE]))])
def read_membresias(
    id_cliente: Optional[int] = Query(None, description="Filtrar por cliente"), 
    estado: Optional[bool] = Query(None, description="Filtrar activas o suspendidas"),
    page: int = Query(1, ge=1), 
    page_size: int = Query(10, ge=1),
    db: Session = Depends(get_db)
):
    return membresia_service.obtener_membresias_paginadas(db=db, page=page, page_size=page_size, id_cliente=id_cliente, estado=estado)

@router.patch("/{id_membresia}", response_model=membresia_schema.MembresiaResponse, summary="Actualizar membresía", dependencies=[Depends(VerificarRol([ADMIN, FINANZAS]))])
def update_membresia(*, db: Session = Depends(get_db), id_membresia: int, membresia_in: membresia_schema.MembresiaUpdate):
    return membresia_service.actualizar_membresia(db=db, id_membresia=id_membresia, membresia_in=membresia_in)
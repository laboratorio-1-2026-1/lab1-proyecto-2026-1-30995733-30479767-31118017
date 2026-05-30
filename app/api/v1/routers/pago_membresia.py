from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import Optional
from app.schemas import pago_membresia_schema
from app.db.database import get_db
from app.services import pago_membresia_service
from app.api.dependencies import VerificarRol, ADMIN, FINANZAS, CLIENTE

router = APIRouter()

@router.post("/", response_model=pago_membresia_schema.PagoMembresiaResponse, summary="Crear pago de membresía", status_code=status.HTTP_201_CREATED, dependencies=[Depends(VerificarRol([ADMIN, FINANZAS]))])
def create_pago(*, db: Session = Depends(get_db), pago_in: pago_membresia_schema.PagoMembresiaCreate):
    return pago_membresia_service.crear_pago(db=db, pago_in=pago_in)

@router.get("/", response_model=pago_membresia_schema.PagoMembresiaPaginatedResponse, summary="Obtener pagos de membresía", dependencies=[Depends(VerificarRol([ADMIN, FINANZAS, CLIENTE]))])
def read_pagos(
    id_cliente: Optional[int] = Query(None, description="Filtrar auditoría por ID de cliente"), 
    page: int = Query(1, ge=1), 
    page_size: int = Query(10, ge=1),
    db: Session = Depends(get_db)
):
    return pago_membresia_service.obtener_pago_membresias_paginados(db=db, page=page, page_size=page_size, id_cliente=id_cliente)

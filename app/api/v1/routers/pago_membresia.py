from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import math
from typing import List

from app.schemas import pago_membresia_schema
from app.crud.crud_pago_membresia import pago_membresia as crud_pago_membresia
from app.db.database import get_db

router = APIRouter()

@router.post("/", response_model=pago_membresia_schema.PagoMembresiaResponse, status_code=status.HTTP_201_CREATED)
def create_pago(
    *,
    db: Session = Depends(get_db),
    pago_in: pago_membresia_schema.PagoMembresiaCreate
):
    if pago_in.monto_membresia <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El monto del pago debe ser mayor a 0."
        )

    if pago_in.referencia:
        pago_existente = crud_pago_membresia.get_by_referencia(db, referencia=pago_in.referencia)
        if pago_existente:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Esta referencia de pago ya se encuentra registrada en el sistema."
            )

    nuevo_pago = crud_pago_membresia.create(db, obj_in=pago_in.model_dump())
    return nuevo_pago

@router.get("/", response_model=pago_membresia_schema.PagoMembresiaPaginatedResponse)
def read_pagos(db: Session = Depends(get_db), page: int = 1, page_size: int = 10):
    if page < 1 or page_size < 1:
        raise HTTPException(status_code=400, detail="Los parámetros de página deben ser mayores a 0.")
    
    total_rows = db.query(crud_pago_membresia.model).count()
    total_pages = math.ceil(total_rows / page_size) if total_rows > 0 else 1
    
    skip = (page - 1) * page_size
    pagos = crud_pago_membresia.get_multi(db, skip=skip, limit=page_size)
    
    return {
        "meta": {"total_rows": total_rows, "current_page": page, "page_size": page_size, "total_pages": total_pages},
        "rows": pagos
    }
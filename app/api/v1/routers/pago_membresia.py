from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
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

@router.get("/", response_model=List[pago_membresia_schema.PagoMembresiaResponse])
def read_pagos(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    pagos = crud_pago_membresia.get_multi(db, skip=skip, limit=limit)
    return pagos
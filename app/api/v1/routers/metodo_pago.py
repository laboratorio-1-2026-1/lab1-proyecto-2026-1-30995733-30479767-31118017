from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# Importación de esquemas ya creados y lógica CRUD
from app.schemas import metodo_pago_schema
from app.crud.crud_metodo_pago import metodo_pago as crud_metodo_pago
from app.db.database import get_db

router = APIRouter()

@router.post("/", response_model=metodo_pago_schema.MetodoPagoResponse, status_code=status.HTTP_201_CREATED)
def create_metodo_pago(
    *,
    db: Session = Depends(get_db),
    metodo_in: metodo_pago_schema.MetodoPagoCreate
):

    nombre_limpio = metodo_in.nombre_metodo.strip()
    if not nombre_limpio:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre del método de pago es obligatorio y no puede contener únicamente espacios en blanco."
        )
    
    metodo_existente = crud_metodo_pago.get_by_nombre(db, nombre_metodo=nombre_limpio)
    if metodo_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El método de pago '{nombre_limpio}' ya está registrado en el sistema."
        )
    
    datos_insercion = metodo_in.model_dump()
    datos_insercion["nombre_metodo"] = nombre_limpio
    
    nuevo_metodo = crud_metodo_pago.create(db, obj_in=datos_insercion)
    return nuevo_metodo

@router.get("/", response_model=List[metodo_pago_schema.MetodoPagoResponse])
def read_metodos_pago(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    metodos = crud_metodo_pago.get_multi(db, skip=skip, limit=limit)
    return metodos
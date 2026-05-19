from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas import cliente_schema
from app.crud.crud_cliente import cliente as crud_cliente
from app.db.database import get_db

router = APIRouter()

@router.post("/", response_model=cliente_schema.ClienteResponse)
def create_cliente(
    *,
    db: Session = Depends(get_db),
    cliente_in: cliente_schema.ClienteCreate
):
    """
    Registra un nuevo cliente en el sistema.
    """
    nuevo_cliente = crud_cliente.create(db, obj_in=cliente_in.model_dump())
    return nuevo_cliente

@router.get("/", response_model=List[cliente_schema.ClienteResponse])
def read_clientes(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    clientes = crud_cliente.get_multi(db, skip=skip, limit=limit)
    return clientes
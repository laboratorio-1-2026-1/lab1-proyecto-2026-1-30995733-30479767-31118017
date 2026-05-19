from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas import producto_schema
from app.crud.crud_producto import producto as crud_producto
from app.db.database import get_db

router = APIRouter()

@router.post("/", response_model=producto_schema.ProductoResponse)
def create_producto(
    *,
    db: Session = Depends(get_db),
    producto_in: producto_schema.ProductoCreate
):
    if producto_in.stock < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El stock de un producto no puede ser negativo."
        )
    if producto_in.precio <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El precio del producto debe ser estrictamente mayor a cero."
        )
        
    nuevo_producto = crud_producto.create(db, obj_in=producto_in.model_dump())
    return nuevo_producto

@router.get("/", response_model=List[producto_schema.ProductoResponse])
def read_productos(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):

    productos = crud_producto.get_multi(db, skip=skip, limit=limit)
    return productos
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import math
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

@router.get("/", response_model=producto_schema.ProductoPaginatedResponse)
def read_productos(db: Session = Depends(get_db), page: int = 1, page_size: int = 10):
    if page < 1 or page_size < 1:
        raise HTTPException(status_code=400, detail="Los parámetros de página deben ser mayores a 0.")
    
    total_rows = db.query(crud_producto.model).count()
    total_pages = math.ceil(total_rows / page_size) if total_rows > 0 else 1
    
    skip = (page - 1) * page_size
    productos = crud_producto.get_multi(db, skip=skip, limit=page_size)
    
    return {
        "meta": {"total_rows": total_rows, "current_page": page, "page_size": page_size, "total_pages": total_pages},
        "rows": productos
    }
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import math
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
    nuevo_cliente = crud_cliente.create(db, obj_in=cliente_in.model_dump())
    return nuevo_cliente

@router.get("/", response_model=cliente_schema.ClientePaginatedResponse)
def read_clientes(db: Session = Depends(get_db), page: int = 1, page_size: int = 10):
    if page < 1 or page_size < 1:
        raise HTTPException(status_code=400, detail="Los parámetros de página deben ser mayores a 0.")
    
    total_rows = db.query(crud_cliente.model).count()
    total_pages = math.ceil(total_rows / page_size) if total_rows > 0 else 1
    
    skip = (page - 1) * page_size
    clientes = crud_cliente.get_multi(db, skip=skip, limit=page_size)
    
    return {
        "meta": {"total_rows": total_rows, "current_page": page, "page_size": page_size, "total_pages": total_pages},
        "rows": clientes
    }
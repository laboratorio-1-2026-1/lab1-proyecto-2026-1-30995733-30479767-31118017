from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import math
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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El nombre del método de pago es obligatorio.")
    
    metodo_existente = crud_metodo_pago.get_by_nombre(db, nombre_metodo=nombre_limpio)
    if metodo_existente:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"El método de pago '{nombre_limpio}' ya está registrado.")
    
    datos_insercion = metodo_in.model_dump()
    datos_insercion["nombre_metodo"] = nombre_limpio
    
    nuevo_metodo = crud_metodo_pago.create(db, obj_in=datos_insercion)
    return nuevo_metodo

@router.get("/", response_model=metodo_pago_schema.MetodoPagoPaginatedResponse)
def read_metodos_pago(db: Session = Depends(get_db), page: int = 1, page_size: int = 10):
    if page < 1 or page_size < 1:
        raise HTTPException(status_code=400, detail="Los parámetros de página deben ser mayores a 0.")
    
    total_rows = db.query(crud_metodo_pago.model).count()
    total_pages = math.ceil(total_rows / page_size) if total_rows > 0 else 1
    
    skip = (page - 1) * page_size
    metodos = crud_metodo_pago.get_multi(db, skip=skip, limit=page_size)
    
    return {
        "meta": {"total_rows": total_rows, "current_page": page, "page_size": page_size, "total_pages": total_pages},
        "rows": metodos
    }
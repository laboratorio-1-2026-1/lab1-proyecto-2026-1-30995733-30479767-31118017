from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import math
from typing import List

from app.schemas import rol_schema
from app.crud.crud_rol import rol as crud_rol
from app.db.database import get_db 

router = APIRouter()

@router.post("/", response_model=rol_schema.RolResponse)
def create_rol(
    *,
    db: Session = Depends(get_db),
    rol_in: rol_schema.RolCreate
):
    rol_existente = db.query(crud_rol.model).filter(crud_rol.model.nombre_rol == rol_in.nombre_rol).first()
    
    if rol_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El rol '{rol_in.nombre_rol}' ya se encuentra registrado en el sistema."
        )
    nuevo_rol = crud_rol.create(db, obj_in=rol_in.model_dump())
    return nuevo_rol

@router.get("/", response_model=rol_schema.RolPaginatedResponse)
def read_roles(db: Session = Depends(get_db), page: int = 1, page_size: int = 10):
    if page < 1 or page_size < 1:
        raise HTTPException(status_code=400, detail="Los parámetros de página deben ser mayores a 0.")
    
    total_rows = db.query(crud_rol.model).count()
    total_pages = math.ceil(total_rows / page_size) if total_rows > 0 else 1
    
    skip = (page - 1) * page_size
    roles = crud_rol.get_multi(db, skip=skip, limit=page_size)
    
    return {
        "meta": {"total_rows": total_rows, "current_page": page, "page_size": page_size, "total_pages": total_pages},
        "rows": roles
    }
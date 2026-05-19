from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import math
from typing import List
from app.schemas import usuario_schema
from app.crud.crud_usuario import usuario as crud_usuario
from app.db.database import get_db 

router = APIRouter()

@router.post("/", response_model=usuario_schema.UsuarioResponse)
def create_user(
    *,
    db: Session = Depends(get_db),
    user_in: usuario_schema.UsuarioCreate
):
    """
    Crea un nuevo usuario en el sistema.
    """
    user = crud_usuario.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="El usuario con este correo ya existe en el sistema.",
        )
    
    user = crud_usuario.create_user(db, obj_in=user_in.model_dump())
    return user

@router.get("/", response_model=usuario_schema.UsuarioPaginatedResponse)
def read_users(db: Session = Depends(get_db), page: int = 1, page_size: int = 10):
    if page < 1 or page_size < 1:
        raise HTTPException(status_code=400, detail="Los parámetros de página deben ser mayores a 0.")
    
    total_rows = db.query(crud_usuario.model).count()
    total_pages = math.ceil(total_rows / page_size) if total_rows > 0 else 1
    
    skip = (page - 1) * page_size
    users = crud_usuario.get_multi(db, skip=skip, limit=page_size)
    
    return {
        "meta": {"total_rows": total_rows, "current_page": page, "page_size": page_size, "total_pages": total_pages},
        "rows": users
    }
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
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

@router.get("/", response_model=List[usuario_schema.UsuarioResponse])
def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Lista todos los usuarios registrados.
    """
    users = crud_usuario.get_multi(db, skip=skip, limit=limit)
    return users
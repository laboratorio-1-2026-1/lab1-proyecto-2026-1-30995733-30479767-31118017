from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
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

@router.get("/", response_model=List[rol_schema.RolResponse])
def read_roles(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Obtiene la lista de todos los roles disponibles en la base de datos.
    """
    roles = crud_rol.get_multi(db, skip=skip, limit=limit)
    return roles
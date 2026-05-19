from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.membresia_schema import MembresiaCreate, MembresiaResponse
from app.crud.crud_membresia import membresia as crud_membresia
from app.db.database import get_db 

router = APIRouter()

@router.post("/", response_model=MembresiaResponse, status_code=status.HTTP_201_CREATED)
def create_membresia(
    *,
    db: Session = Depends(get_db),
    membresia_in: MembresiaCreate
):

    if membresia_in.fecha_fin <= membresia_in.fecha_inicio:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error de consistencia: La fecha de finalización debe ser posterior a la fecha de inicio."
        )
    
    obj_data = membresia_in.model_dump()
    if isinstance(obj_data.get("estado"), str):
        obj_data["estado"] = obj_data["estado"].lower() in ["activa", "activo", "true", "1"]
    
    nueva_membresia = crud_membresia.create(db, obj_in=obj_data)
    
    nueva_membresia.estado = "Activa" if nueva_membresia.estado else "Inactiva"
    return nueva_membresia


@router.get("/", response_model=List[MembresiaResponse])
def read_membresias(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):

    membresias = crud_membresia.get_multi(db, skip=skip, limit=limit)
    
    for m in membresias:
        m.estado = "Activa" if m.estado else "Inactiva"
        
    return membresias


@router.get("/{id_membresia}", response_model=MembresiaResponse)
def read_membresia_by_id(
    id_membresia: int,
    db: Session = Depends(get_db)
):
    membresia_db = crud_membresia.get(db, id=id_membresia)
    if not membresia_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Membresía con ID {id_membresia} no encontrada."
        )
    
    membresia_db.estado = "Activa" if membresia_db.estado else "Inactiva"
    return membresia_db



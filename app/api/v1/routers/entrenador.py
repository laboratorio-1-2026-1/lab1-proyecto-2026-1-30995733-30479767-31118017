from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas import entrenador_schema
from app.crud.crud_entrenador import entrenador as crud_entrenador
from app.db.database import get_db
from app.api.dependencies import get_current_user
from app.models.usuario import Usuario

router = APIRouter()

@router.post("/", response_model=entrenador_schema.EntrenadorResponse)
def create_entrenador(
    *,
    db: Session = Depends(get_db),
    entrenador_in: entrenador_schema.EntrenadorCreate,
    current_user: Usuario = Depends(get_current_user)
):
    nuevo_entrenador = crud_entrenador.create(db, obj_in=entrenador_in.model_dump())
    return nuevo_entrenador

@router.get("/", response_model=List[entrenador_schema.EntrenadorResponse])
def read_entrenadores(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    entrenadores = crud_entrenador.get_multi(db, skip=skip, limit=limit)
    return entrenadores
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.schemas import entrenador_schema
from app.db.database import get_db
from app.services import entrenador_service
from app.api.dependencies import VerificarRol, ADMIN, CLIENTE, FINANZAS, ENTRENADOR

router = APIRouter()

@router.post("/", response_model=entrenador_schema.EntrenadorResponse, summary="Crear entrenador", dependencies=[Depends(VerificarRol([ADMIN]))])
def create_entrenador(*, db: Session = Depends(get_db), entrenador_in: entrenador_schema.EntrenadorCreate):
    return entrenador_service.crear_entrenador(db=db, entrenador_in=entrenador_in)

@router.get("/", response_model=entrenador_schema.EntrenadorPaginatedResponse, summary="Obtener entrenadores", dependencies=[Depends(VerificarRol([ADMIN, CLIENTE, FINANZAS, ENTRENADOR]))])
def read_entrenadores(
    especialidad: Optional[str] = Query(None, description="Filtrar por área de especialidad"), 
    page: int = Query(1, ge=1), 
    page_size: int = Query(10, ge=1),
    db: Session = Depends(get_db)
):
    return entrenador_service.obtener_entrenadores_paginados(db=db, page=page, page_size=page_size, especialidad=especialidad)

@router.patch("/{id_entrenador}", response_model=entrenador_schema.EntrenadorResponse, summary="Actualizar entrenador", dependencies=[Depends(VerificarRol([ADMIN]))])
def update_entrenador(*, db: Session = Depends(get_db), id_entrenador: int, entrenador_in: entrenador_schema.EntrenadorUpdate):
    return entrenador_service.actualizar_entrenador(db=db, id_entrenador=id_entrenador, entrenador_in=entrenador_in)
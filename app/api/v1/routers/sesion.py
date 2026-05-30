from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from app.schemas import sesion_clase_schema
from app.db.database import get_db 
from app.services import sesion_service
from app.api.dependencies import VerificarRol, ADMIN, ENTRENADOR, CLIENTE, FINANZAS

router = APIRouter()

@router.post("/", response_model=sesion_clase_schema.SesionClaseResponse, summary="Crear sesión", dependencies=[Depends(VerificarRol([ADMIN]))])
def create_sesion(*, db: Session = Depends(get_db), sesion_in: sesion_clase_schema.SesionClaseCreate):
    return sesion_service.crear_sesion(db=db, sesion_in=sesion_in)

@router.get("/", response_model=sesion_clase_schema.SesionClasePaginatedResponse, summary="Obtener sesiones", dependencies=[Depends(VerificarRol([ADMIN, ENTRENADOR, CLIENTE, FINANZAS]))])
def read_sesiones(
    id_disciplina: Optional[int] = None, 
    id_entrenador: Optional[int] = None,
    page: int = 1, 
    page_size: int = 10,
    db: Session = Depends(get_db)
):
    return sesion_service.obtener_sesiones_paginadas(db=db, page=page, page_size=page_size, id_disciplina=id_disciplina, id_entrenador=id_entrenador)

@router.patch("/{id_sesion}", response_model=sesion_clase_schema.SesionClaseResponse, summary="Actualizar sesión", dependencies=[Depends(VerificarRol([ADMIN]))])
def update_sesion(*, db: Session = Depends(get_db), id_sesion: int, sesion_in: sesion_clase_schema.SesionClaseUpdate):
    return sesion_service.actualizar_sesion(db=db, id_sesion=id_sesion, sesion_in=sesion_in)
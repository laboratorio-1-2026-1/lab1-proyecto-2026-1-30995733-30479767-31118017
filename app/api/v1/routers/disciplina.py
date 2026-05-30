from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.schemas import disciplina_schema
from app.db.database import get_db 
from app.services import disciplina_service
from app.api.dependencies import VerificarRol, ADMIN, ENTRENADOR, CLIENTE, FINANZAS

router = APIRouter()

@router.post("/", response_model=disciplina_schema.DisciplinaResponse, summary="Crear disciplina", dependencies=[Depends(VerificarRol([ADMIN]))])
def create_disciplina(*, db: Session = Depends(get_db), disciplina_in: disciplina_schema.DisciplinaCreate):
    return disciplina_service.crear_disciplina(db=db, disciplina_in=disciplina_in)

@router.get("/", response_model=disciplina_schema.DisciplinaPaginatedResponse, summary="Obtener disciplinas", dependencies=[Depends(VerificarRol([ADMIN, ENTRENADOR, CLIENTE, FINANZAS]))])
def read_disciplinas(
    nombre: Optional[str] = Query(None, description="Filtrar por nombre exacto o parcial"),
    page: int = Query(1, ge=1), 
    page_size: int = Query(10, ge=1),
    db: Session = Depends(get_db)
):
    return disciplina_service.obtener_disciplinas_paginadas(db=db, page=page, page_size=page_size, nombre=nombre)

@router.patch("/{id_disciplina}", response_model=disciplina_schema.DisciplinaResponse, summary="Actualizar disciplina", dependencies=[Depends(VerificarRol([ADMIN]))])
def update_disciplina(*, db: Session = Depends(get_db), id_disciplina: int, disciplina_in: disciplina_schema.DisciplinaUpdate):
    return disciplina_service.actualizar_disciplina(db=db, id_disciplina=id_disciplina, disciplina_in=disciplina_in)
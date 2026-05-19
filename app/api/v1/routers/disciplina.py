from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.schemas import disciplina_schema
from app.crud.crud_disciplina import disciplina as crud_disciplina
from app.db.database import get_db 

router = APIRouter()

@router.post("/", response_model=disciplina_schema.DisciplinaResponse)
def create_disciplina(
    *,
    db: Session = Depends(get_db),
    disciplina_in: disciplina_schema.DisciplinaCreate
):
    nueva_disciplina = crud_disciplina.create(db, obj_in=disciplina_in.model_dump())
    return nueva_disciplina

@router.get("/", response_model=List[disciplina_schema.DisciplinaResponse])
def read_disciplinas(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    disciplinas = crud_disciplina.get_multi(db, skip=skip, limit=limit)
    return disciplinas
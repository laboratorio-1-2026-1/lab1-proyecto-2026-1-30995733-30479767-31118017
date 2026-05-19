from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import math
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

@router.get("/", response_model=disciplina_schema.DisciplinaPaginatedResponse)
def read_disciplinas(db: Session = Depends(get_db), page: int = 1, page_size: int = 10):
    if page < 1 or page_size < 1:
        raise HTTPException(status_code=400, detail="Los parámetros de página deben ser mayores a 0.")
    
    total_rows = db.query(crud_disciplina.model).count()
    total_pages = math.ceil(total_rows / page_size) if total_rows > 0 else 1
    
    skip = (page - 1) * page_size
    disciplinas = crud_disciplina.get_multi(db, skip=skip, limit=page_size)
    
    return {
        "meta": {"total_rows": total_rows, "current_page": page, "page_size": page_size, "total_pages": total_pages},
        "rows": disciplinas
    }
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import math
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

@router.get("/", response_model=entrenador_schema.EntrenadorPaginatedResponse)
def read_entrenadores(db: Session = Depends(get_db), page: int = 1, page_size: int = 10):
    if page < 1 or page_size < 1:
        raise HTTPException(status_code=400, detail="Los parámetros de página deben ser mayores a 0.")
    
    total_rows = db.query(crud_entrenador.model).count()
    total_pages = math.ceil(total_rows / page_size) if total_rows > 0 else 1
    
    skip = (page - 1) * page_size
    entrenadores = crud_entrenador.get_multi(db, skip=skip, limit=page_size)
    
    return {
        "meta": {"total_rows": total_rows, "current_page": page, "page_size": page_size, "total_pages": total_pages},
        "rows": entrenadores
    }
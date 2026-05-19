from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import math
from app.schemas import categoria_maquina_schema
from app.crud.crud_categoria import categoria as crud_categoria
from app.db.database import get_db 

router = APIRouter()

@router.post("/", response_model=categoria_maquina_schema.CategoriaMaquinaResponse)
def create_categoria(
    *,
    db: Session = Depends(get_db),
    obj_in: categoria_maquina_schema.CategoriaMaquinaCreate
):
    return crud_categoria.create(db, obj_in=obj_in.model_dump())

@router.get("/", response_model=categoria_maquina_schema.CategoriaMaquinaPaginatedResponse)
def read_categorias(db: Session = Depends(get_db), page: int = 1, page_size: int = 10):
    if page < 1 or page_size < 1:
        raise HTTPException(status_code=400, detail="Los parámetros de página deben ser mayores a 0.")
    
    total_rows = db.query(crud_categoria.model).count()
    total_pages = math.ceil(total_rows / page_size) if total_rows > 0 else 1
    skip = (page - 1) * page_size
    categorias = crud_categoria.get_multi(db, skip=skip, limit=page_size)
    return {
        "meta": {"total_rows": total_rows, "current_page": page, "page_size": page_size, "total_pages": total_pages},
        "rows": categorias
    }
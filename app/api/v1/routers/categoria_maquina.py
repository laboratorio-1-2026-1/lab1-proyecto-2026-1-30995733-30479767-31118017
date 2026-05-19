from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
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

@router.get("/", response_model=List[categoria_maquina_schema.CategoriaMaquinaResponse])
def read_categorias(db: Session = Depends(get_db)):
    return crud_categoria.get_multi(db)
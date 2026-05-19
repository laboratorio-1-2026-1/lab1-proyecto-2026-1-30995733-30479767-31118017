from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import math
from app.api.dependencies import get_current_user 
from app.models.usuario import Usuario
from app.schemas import maquina_schema
from app.crud.crud_maquina import maquina as crud_maquina
from app.db.database import get_db 

router = APIRouter()

@router.post("/", response_model=maquina_schema.MaquinaResponse)
def create_maquina(
    *,
    db: Session = Depends(get_db),
    maquina_in: maquina_schema.MaquinaCreate,
    current_user: Usuario = Depends(get_current_user)
):
    nueva_maquina = crud_maquina.create(db, obj_in=maquina_in.model_dump())
    return nueva_maquina

@router.get("/", response_model=maquina_schema.MaquinaPaginatedResponse)
def read_maquinas(db: Session = Depends(get_db), page: int = 1, page_size: int = 10):
    if page < 1 or page_size < 1:
        raise HTTPException(status_code=400, detail="Los parámetros de página deben ser mayores a 0.")
    
    total_rows = db.query(crud_maquina.model).count()
    total_pages = math.ceil(total_rows / page_size) if total_rows > 0 else 1
    
    skip = (page - 1) * page_size
    maquinas = crud_maquina.get_multi(db, skip=skip, limit=page_size)
    
    return {
        "meta": {"total_rows": total_rows, "current_page": page, "page_size": page_size, "total_pages": total_pages},
        "rows": maquinas
    }

@router.put("/{id_maquina}", response_model=maquina_schema.MaquinaResponse)
def update_maquina(*, db: Session = Depends(get_db), id_maquina: int, maquina_in: maquina_schema.MaquinaUpdate, current_user: Usuario = Depends(get_current_user)):
    maquina_actual = crud_maquina.get(db=db, id=id_maquina)
    if not maquina_actual:
        raise HTTPException(status_code=404, detail="Error: Máquina no encontrada")
    return crud_maquina.update(db=db, db_obj=maquina_actual, obj_in=maquina_in)

@router.delete("/{id_maquina}", response_model=maquina_schema.MaquinaResponse)
def delete_maquina(*, db: Session = Depends(get_db), id_maquina: int, current_user: Usuario = Depends(get_current_user)):
    maquina_actual = crud_maquina.get(db=db, id=id_maquina)
    if not maquina_actual:
        raise HTTPException(status_code=404, detail="Error: Máquina no encontrada")
    return crud_maquina.remove(db=db, id=id_maquina)
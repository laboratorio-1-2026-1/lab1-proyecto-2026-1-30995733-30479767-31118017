from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
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

@router.get("/", response_model=List[maquina_schema.MaquinaResponse])
def read_maquinas(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    maquinas = crud_maquina.get_multi(db, skip=skip, limit=limit)
    return maquinas













@router.put("/{id_maquina}", response_model=maquina_schema.MaquinaResponse)
def update_maquina(
    *,
    db: Session = Depends(get_db),
    id_maquina: int,
    maquina_in: maquina_schema.MaquinaUpdate,
    current_user: Usuario = Depends(get_current_user)
):
    """
    Actualiza los datos de una máquina existente.
    """
    # 1. Buscamos si la máquina existe en la base de datos
    maquina_actual = crud_maquina.get(db=db, id=id_maquina)
    if not maquina_actual:
        raise HTTPException(status_code=404, detail="Error: Máquina no encontrada")
    
    # 2. Usamos el superpoder 'update' de tu base.py
    maquina_actualizada = crud_maquina.update(db=db, db_obj=maquina_actual, obj_in=maquina_in)
    return maquina_actualizada


# --- ENDPOINT PARA ELIMINAR (DELETE) ---
@router.delete("/{id_maquina}", response_model=maquina_schema.MaquinaResponse)
def delete_maquina(
    *,
    db: Session = Depends(get_db),
    id_maquina: int,
    current_user: Usuario = Depends(get_current_user)
):
    """
    Elimina una máquina del inventario.
    """
    # 1. Buscamos si la máquina existe
    maquina_actual = crud_maquina.get(db=db, id=id_maquina)
    if not maquina_actual:
        raise HTTPException(status_code=404, detail="Error: Máquina no encontrada")
    
    # 2. Usamos el superpoder 'remove' de tu base.py
    maquina_eliminada = crud_maquina.remove(db=db, id=id_maquina)
    return maquina_eliminada
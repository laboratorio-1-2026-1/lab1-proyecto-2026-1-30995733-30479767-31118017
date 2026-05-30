from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.schemas import maquina_schema
from app.db.database import get_db 
from app.services import maquina_service
from app.api.dependencies import VerificarRol, ADMIN, ENTRENADOR, CLIENTE, FINANZAS

router = APIRouter()

@router.post("/", response_model=maquina_schema.MaquinaResponse, summary="Crear máquina", dependencies=[Depends(VerificarRol([ADMIN]))])
def create_maquina(*, db: Session = Depends(get_db), maquina_in: maquina_schema.MaquinaCreate):
    return maquina_service.crear_maquina(db=db, maquina_in=maquina_in)

@router.get("/", response_model=maquina_schema.MaquinaPaginatedResponse, summary="Obtener máquinas", dependencies=[Depends(VerificarRol([ADMIN, ENTRENADOR, CLIENTE, FINANZAS]))])
def read_maquinas(
    estado_maquina: Optional[str] = Query(None, description="Filtrar por estado de la máquina"), 
    id_categoria: Optional[int] = Query(None, description="Filtrar por ID de categoría"),   
    page: int = Query(1, ge=1), 
    page_size: int = Query(10, ge=1),
    db: Session = Depends(get_db)
):
    return maquina_service.obtener_maquinas_paginadas(
        db=db, 
        page=page, 
        page_size=page_size, 
        estado=estado_maquina, 
        id_cat=id_categoria
    )

@router.patch("/{id_maquina}", response_model=maquina_schema.MaquinaResponse, summary="Actualizar máquina", dependencies=[Depends(VerificarRol([ADMIN]))])
def update_maquina(*, db: Session = Depends(get_db), id_maquina: int, maquina_in: maquina_schema.MaquinaUpdate):
    return maquina_service.actualizar_maquina(db=db, id_maquina=id_maquina, maquina_in=maquina_in)
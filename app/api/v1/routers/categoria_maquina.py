from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from app.schemas import categoria_maquina_schema
from app.db.database import get_db 
from app.services import categoria_maquina_service
from app.api.dependencies import VerificarRol, ADMIN, ENTRENADOR, CLIENTE, FINANZAS

router = APIRouter()

@router.post("/", response_model=categoria_maquina_schema.CategoriaMaquinaResponse, summary="Crear categoría de máquina", dependencies=[Depends(VerificarRol([ADMIN]))])
def create_categoria(*, db: Session = Depends(get_db), obj_in: categoria_maquina_schema.CategoriaMaquinaCreate):
    return categoria_maquina_service.crear_categoria(db=db, obj_in=obj_in)

@router.get("/", response_model=categoria_maquina_schema.CategoriaMaquinaPaginatedResponse, summary="Obtener categorías de máquinas", dependencies=[Depends(VerificarRol([ADMIN, ENTRENADOR, CLIENTE, FINANZAS]))])
def read_categorias(
    nombre: Optional[str] = None,
    page: int = 1, 
    page_size: int = 10,
    db: Session = Depends(get_db)
):
    return categoria_maquina_service.obtener_categorias_paginadas(db=db, page=page, page_size=page_size, nombre_filtro=nombre)

@router.patch("/{id_categoria}", response_model=categoria_maquina_schema.CategoriaMaquinaResponse, summary="Actualizar categoría de máquina", dependencies=[Depends(VerificarRol([ADMIN]))])
def update_categoria(*, db: Session = Depends(get_db), id_categoria: int, obj_in: categoria_maquina_schema.CategoriaMaquinaUpdate):
    return categoria_maquina_service.actualizar_categoria(db=db, id_categoria=id_categoria, categoria_in=obj_in)

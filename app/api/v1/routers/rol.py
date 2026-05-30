from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional, Annotated
from app.schemas import rol_schema
from app.db.database import get_db 
from app.services import rol_service
from app.api.dependencies import VerificarRol, ADMIN

router = APIRouter()

@router.post("/", response_model=rol_schema.RolResponse, summary="Crear rol", dependencies=[Depends(VerificarRol([ADMIN]))])
def create_rol(*, db: Session = Depends(get_db), rol_in: rol_schema.RolCreate):
    return rol_service.crear_rol(db=db, rol_in=rol_in)

@router.get("/", response_model=rol_schema.RolPaginatedResponse, summary="Obtener roles", dependencies=[Depends(VerificarRol([ADMIN]))])
def read_roles(
    nombre: Optional[str] = None, 
    page: int = 1, 
    page_size: int = 10,
    db: Session = Depends(get_db)
):
    return rol_service.obtener_roles_paginados(db=db, page=page, page_size=page_size, nombre_filtro=nombre)

@router.patch("/{id_rol}", response_model=rol_schema.RolResponse, summary="Actualizar rol", dependencies=[Depends(VerificarRol([ADMIN]))])
def update_rol(*, db: Session = Depends(get_db), id_rol: int, rol_in: rol_schema.RolUpdate):
    return rol_service.actualizar_rol(db=db, id_rol=id_rol, rol_in=rol_in)
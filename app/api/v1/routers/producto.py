from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from app.schemas import producto_schema
from app.db.database import get_db
from app.services import producto_service
from app.api.dependencies import VerificarRol, ADMIN, FINANZAS, CLIENTE, ENTRENADOR

router = APIRouter()

@router.post("/", response_model=producto_schema.ProductoResponse, summary="Crear producto", dependencies=[Depends(VerificarRol([ADMIN, FINANZAS]))])
def create_producto(*, db: Session = Depends(get_db), producto_in: producto_schema.ProductoCreate):
    return producto_service.crear_producto(db=db, producto_in=producto_in)

@router.get("/", response_model=producto_schema.ProductoPaginatedResponse, summary="Lista de productos", dependencies=[Depends(VerificarRol([ADMIN, FINANZAS, CLIENTE, ENTRENADOR]))])
def read_productos(
    nombre_prod: Optional[str] = None, 
    page: int = 1, 
    page_size: int = 10,
    db: Session = Depends(get_db)
):
    return producto_service.obtener_productos_paginados(db=db, page=page, page_size=page_size, nombre=nombre_prod)

@router.patch("/{id_producto}", response_model=producto_schema.ProductoResponse, summary="Actualizar producto", dependencies=[Depends(VerificarRol([ADMIN, FINANZAS]))])
def update_producto(*, db: Session = Depends(get_db), id_producto: int, producto_in: producto_schema.ProductoUpdate):
    return producto_service.actualizar_producto(db=db, id_producto=id_producto, producto_in=producto_in)
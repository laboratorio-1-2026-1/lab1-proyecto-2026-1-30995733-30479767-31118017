from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Optional
from app.schemas import venta_producto_schema
from app.db.database import get_db
from app.services import venta_producto_service
from app.api.dependencies import VerificarRol, ADMIN, FINANZAS

router = APIRouter()

@router.post("/", response_model=venta_producto_schema.VentaProductoResponse, summary="Crear venta de producto", dependencies=[Depends(VerificarRol([ADMIN, FINANZAS]))])
def create_venta_producto(
    *,
    db: Session = Depends(get_db),
    venta_in: venta_producto_schema.VentaProductoCreate
):
    return venta_producto_service.crear_venta(db=db, venta_in=venta_in)

@router.get("/", response_model=venta_producto_schema.VentaProductoPaginatedResponse, summary="Obtener ventas de producto", dependencies=[Depends(VerificarRol([ADMIN, FINANZAS]))])
def read_ventas_producto(
    id_cliente: Optional[int] = None,
    page: int = 1, 
    page_size: int = 10,
    db: Session = Depends(get_db)
):
    return venta_producto_service.obtener_ventas_paginadas(db=db, page=page, page_size=page_size, id_cliente=id_cliente)

@router.patch("/{id_venta}/completar", response_model=venta_producto_schema.VentaProductoResponse, summary="Completar venta de producto", dependencies=[Depends(VerificarRol([ADMIN, FINANZAS]))])
def cerrar_factura_venta(*, db: Session = Depends(get_db), id_venta: int):
    return venta_producto_service.completar_venta(db=db, id_venta=id_venta)
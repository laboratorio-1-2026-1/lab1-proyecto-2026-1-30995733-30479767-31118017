from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.api.dependencies import get_current_user 
from app.models.usuario import Usuario
from app.schemas import venta_producto_schema
from app.crud.crud_venta_producto import venta_producto as crud_venta_producto
from app.db.database import get_db

router = APIRouter()

@router.post("/", response_model=venta_producto_schema.VentaProductoResponse)
def create_venta_producto(
    *,
    db: Session = Depends(get_db),
    venta_in: venta_producto_schema.VentaProductoCreate,
    current_user: Usuario = Depends(get_current_user)
):

    if venta_in.monto_total <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error: El monto total de la venta debe ser mayor a cero."
        )
    
    if venta_in.id_metodo != 1 and not venta_in.referencia:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Regla de Negocio: La referencia de pago es obligatoria para métodos distintos al efectivo."
        )

    nueva_venta = crud_venta_producto.create(db=db, obj_in=venta_in.model_dump())
    return nueva_venta


@router.get("/", response_model=List[venta_producto_schema.VentaProductoResponse])
def read_ventas_producto(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: Usuario = Depends(get_current_user)
):

    ventas = crud_venta_producto.get_multi(db, skip=skip, limit=limit)
    return ventas
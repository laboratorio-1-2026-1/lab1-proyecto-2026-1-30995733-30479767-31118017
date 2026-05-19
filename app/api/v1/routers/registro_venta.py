from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.api.dependencies import get_current_user 
from app.models.usuario import Usuario
from app.models.registro_venta import RegistroVenta 
from app.schemas import registro_venta_schema
from app.crud.crud_registro_venta import registro_venta as crud_registro_venta
from app.crud.crud_producto import producto as crud_producto
from app.db.database import get_db

router = APIRouter()

@router.post("/", response_model=registro_venta_schema.RegistroVentaResponse)
def create_registro_venta(
    *,
    db: Session = Depends(get_db),
    registro_in: registro_venta_schema.RegistroVentaCreate,
    current_user: Usuario = Depends(get_current_user)
):

    if registro_in.cantidad <= 0:
        raise HTTPException(status_code=400, detail="Error: La cantidad debe ser mayor a cero.")
    if registro_in.subtotal < 0:
         raise HTTPException(status_code=400, detail="Error: El subtotal no puede ser negativo.")

    producto_db = crud_producto.get(db=db, id=registro_in.id_producto)
    if not producto_db:
        raise HTTPException(status_code=404, detail="Error: El producto solicitado no existe.")


    if producto_db.stock < registro_in.cantidad:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Stock insuficiente. Solo quedan {producto_db.stock} unidades del producto."
        )
    try:
        producto_db.stock -= registro_in.cantidad

        nuevo_registro = RegistroVenta(**registro_in.model_dump())

        db.add(producto_db)
        db.add(nuevo_registro)
        db.commit()
        db.refresh(nuevo_registro)
        
        return nuevo_registro

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error crítico en la transacción. No se descontó el stock. Detalles: {str(e)}"
        )


@router.get("/", response_model=List[registro_venta_schema.RegistroVentaResponse])
def read_registros_venta(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: Usuario = Depends(get_current_user)
):
    registros = crud_registro_venta.get_multi(db, skip=skip, limit=limit)
    return registros
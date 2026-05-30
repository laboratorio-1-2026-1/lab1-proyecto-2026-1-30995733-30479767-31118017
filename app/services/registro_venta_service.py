from fastapi import HTTPException, status
from app.core.exceptions import BadRequestException, ConflictException, NotFoundException
from sqlalchemy.orm import Session
from typing import Optional
from app.core.utils import paginar_resultados
from app.schemas import registro_venta_schema
from app.models.registro_venta_model import RegistroVenta
from app.repositories.registro_venta_repository import registro_venta as crud_registro_venta
from app.repositories.producto_repository import producto as crud_producto 
from app.repositories.venta_producto_repository import venta_producto as crud_venta_producto

def crear_registro_venta(db: Session, registro_in: registro_venta_schema.RegistroVentaCreate):

    if registro_in.cantidad <= 0:
        raise BadRequestException(codigo_interno="ERR_CANTIDAD_INVALIDA", mensaje="La cantidad a comprar debe ser mayor a cero.")

    venta_padre = crud_venta_producto.get(db=db, id=registro_in.id_venta)
    if not venta_padre:
        raise NotFoundException(
            codigo_interno="ERR_VENTA_NO_ENCONTRADA", 
            mensaje="La factura de venta principal especificada no existe en el sistema."
        )

    if venta_padre.estado_venta.lower() == "completada":
        raise ConflictException(
            codigo_interno="ERR_VENTA_CERRADA",
            mensaje="Operación denegada: Esta factura ya fue pagada y cerrada. No se pueden agregar más productos."
        )

    producto_db = crud_producto.get(db=db, id=registro_in.id_producto)
    if not producto_db:
        raise NotFoundException(codigo_interno="ERR_PRODUCTO_NO_ENCONTRADO", mensaje="El producto solicitado no existe.")

    if producto_db.stock < registro_in.cantidad:
        raise ConflictException(
            codigo_interno="ERR_STOCK_INSUFICIENTE",
            mensaje=f"Operación cancelada: Stock insuficiente. Solo quedan {producto_db.stock} unidades de '{producto_db.nombre_prod}'."
        )

    datos_venta = registro_in.model_dump()
    datos_venta["precio_unitario"] = producto_db.precio
    datos_venta["subtotal"] = producto_db.precio * registro_in.cantidad

    try:
        producto_db.stock -= registro_in.cantidad
        nuevo_registro = RegistroVenta(**datos_venta)

        db.add(nuevo_registro)
        db.commit()
        db.refresh(nuevo_registro)
        
        return nuevo_registro
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error crítico en la transacción POS. Rollback ejecutado de emergencia. Detalles: {str(e)}"
        )

def obtener_registros_paginados(db: Session, page: int, page_size: int, id_producto: Optional[int] = None, id_venta: Optional[int] = None):

    query = crud_registro_venta.obtener_query_filtrada(db, id_producto=id_producto, id_venta=id_venta)
    return paginar_resultados(db, crud_registro_venta, page, page_size, query_personalizada=query)
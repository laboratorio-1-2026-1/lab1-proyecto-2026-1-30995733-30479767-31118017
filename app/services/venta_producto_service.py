from fastapi import status
from app.core.exceptions import BadRequestException, NotFoundException, ConflictException
from sqlalchemy.orm import Session
from typing import Optional
from app.core.utils import paginar_resultados
from app.schemas import venta_producto_schema
from app.repositories.venta_producto_repository import venta_producto as crud_venta_producto
from app.repositories.cliente_repository import cliente as crud_cliente
from app.repositories.metodo_pago_repository import metodo_pago as crud_metodo_pago

def crear_venta(db: Session, venta_in: venta_producto_schema.VentaProductoCreate):

    cliente_db = crud_cliente.get(db=db, id=venta_in.id_cliente)
    if not cliente_db:
        raise NotFoundException(codigo_interno="ERR_CLIENTE_NO_ENCONTRADO", mensaje="El cliente ingresado no existe.")
        
    metodo_db = crud_metodo_pago.get(db=db, id=venta_in.id_metodo)
    if not metodo_db:
        raise NotFoundException(codigo_interno="ERR_METODO_NO_ENCONTRADO", mensaje="El método de pago ingresado no existe.")

    if venta_in.id_metodo != 1 and not venta_in.referencia:
        raise BadRequestException(
            codigo_interno="ERR_REFERENCIA_REQUERIDA",
            mensaje="Regla de Negocio: La referencia de pago es obligatoria para métodos distintos al efectivo."
        )
    obj_in = venta_in.model_dump()
    obj_in["monto_total"] = 0.0
    obj_in["estado_venta"] = "Pendiente"

    return crud_venta_producto.create(db=db, obj_in=obj_in)

def completar_venta(db: Session, id_venta: int):
    venta_actual = crud_venta_producto.get(db=db, id=id_venta)
    
    if not venta_actual:
        raise NotFoundException(codigo_interno="ERR_VENTA_NO_ENCONTRADA", mensaje="La factura solicitada no existe.")
        
    if venta_actual.estado_venta.lower() == "Completada".lower():
        raise ConflictException(
            codigo_interno="ERR_VENTA_YA_CERRADA", 
            mensaje="Esta factura ya se encuentra completada y cerrada."
        )
    return crud_venta_producto.update(db=db, db_obj=venta_actual, obj_in={"estado_venta": "Completada"})


def obtener_ventas_paginadas(db: Session, page: int, page_size: int, id_cliente: Optional[int] = None):

    query = crud_venta_producto.obtener_query_filtrada(db, id_cliente=id_cliente)
    
    return paginar_resultados(db, crud_venta_producto, page, page_size, query_personalizada=query)
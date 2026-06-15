from fastapi import status
from app.core.exceptions import BadRequestException, ConflictException, NotFoundException
from sqlalchemy.orm import Session
from typing import Optional
from app.core.utils import paginar_resultados
from app.schemas import pago_membresia_schema
from app.repositories.pago_membresia_repository import pago_membresia as crud_pago_membresia
from app.repositories.cliente_repository import cliente as crud_cliente
from app.repositories.metodo_pago_repository import metodo_pago as crud_metodo_pago

def crear_pago(db: Session, pago_in: pago_membresia_schema.PagoMembresiaCreate):

    if not crud_cliente.get(db=db, id=pago_in.id_cliente):
        raise NotFoundException(codigo_interno="ERR_CLIENTE_NO_ENCONTRADO", mensaje="El cliente asignado al pago no existe.")
    
    if not crud_metodo_pago.get(db=db, id=pago_in.id_metodo):
        raise NotFoundException(codigo_interno="ERR_METODO_NO_ENCONTRADO", mensaje="El método de pago especificado no existe.")

    if pago_in.monto_membresia <= 0:
        raise BadRequestException(codigo_interno="ERR_MONTO_INVALIDO", mensaje="El monto del pago debe ser estrictamente mayor a 0.")

    if pago_in.id_metodo != 1:
        if not pago_in.referencia or not pago_in.referencia.strip():
            raise BadRequestException(
                codigo_interno="ERR_REFERENCIA_REQUERIDA", 
                mensaje="La referencia es obligatoria para pagos con Zelle, Tarjeta de Crédito/Débito, etc."
            )

    if pago_in.referencia and pago_in.referencia.strip():
        referencia_limpia = pago_in.referencia.strip().upper()
        if crud_pago_membresia.get_by_referencia(db, referencia=referencia_limpia):
            raise ConflictException(
                codigo_interno="ERR_REFERENCIA_DUPLICADA",
                mensaje=f"Alerta de Fraude: La referencia de pago '{referencia_limpia}' ya se encuentra registrada."
            )
        pago_in.referencia = referencia_limpia
    else:
        pago_in.referencia = None

    return crud_pago_membresia.create(db, obj_in=pago_in.model_dump())

def obtener_pago_membresias_paginados(db: Session, page: int, page_size: int, id_cliente: Optional[int] = None):
    query = crud_pago_membresia.obtener_query_filtrada(db, id_cliente=id_cliente)
    return paginar_resultados(db, crud_pago_membresia, page, page_size, query_personalizada=query)

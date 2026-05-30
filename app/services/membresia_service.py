from fastapi import status
from app.core.exceptions import BadRequestException, ConflictException, NotFoundException
from sqlalchemy.orm import Session
from app.core.utils import paginar_resultados
from app.schemas import membresia_schema
from typing import Optional
from app.repositories.membresia_repository import membresia as crud_membresia
from app.repositories.cliente_repository import cliente as crud_cliente
from app.repositories.plan_repository import plan as crud_plan
from app.repositories.pago_membresia_repository import pago_membresia as crud_pago_membresia
from datetime import datetime

def crear_membresia(db: Session, membresia_in: membresia_schema.MembresiaCreate):

    if isinstance(membresia_in.fecha_inicio, datetime):
        membresia_in.fecha_inicio = membresia_in.fecha_inicio.date()
    if isinstance(membresia_in.fecha_fin, datetime):
        membresia_in.fecha_fin = membresia_in.fecha_fin.date()

    if membresia_in.fecha_fin <= membresia_in.fecha_inicio:
        raise BadRequestException(
            codigo_interno="ERR_FECHAS_INVALIDAS",
            mensaje="Regla de Negocio: La fecha de finalización de la membresía debe ser posterior a su fecha de inicio."
        )

    if not crud_cliente.get(db=db, id=membresia_in.id_cliente):
        raise NotFoundException(codigo_interno="ERR_CLIENTE_NOT_FOUND", mensaje="El cliente ingresado no existe en el sistema.")
        
    plan_db = crud_plan.get(db=db, id=membresia_in.id_plan)
    if not plan_db:
        raise NotFoundException(codigo_interno="ERR_PLAN_NOT_FOUND", mensaje="El plan de suscripción seleccionado no existe.")
        
    pago_db = crud_pago_membresia.get(db=db, id=membresia_in.id_pago)
    if not pago_db:
        raise NotFoundException(codigo_interno="ERR_PAGO_NOT_FOUND", mensaje="El recibo de pago indicado no existe.")


    if pago_db.id_cliente != membresia_in.id_cliente:
        raise ConflictException(
            codigo_interno="ERR_PAGO_AJENO", 
            mensaje="Intento de Fraude: El recibo de pago ingresado pertenece a otro cliente."
        )

    if crud_membresia.get_by_pago_id(db=db, id_pago=membresia_in.id_pago):
        raise ConflictException(
            codigo_interno="ERR_PAGO_YA_UTILIZADO", 
            mensaje="Operación rechazada: Este recibo de pago ya fue 'gastado' para activar una membresía previamente."
        )

    if pago_db.monto_membresia < plan_db.precio_sub:
        raise BadRequestException(
            codigo_interno="ERR_FONDOS_INSUFICIENTES", 
            mensaje=f"Fondos insuficientes: El plan cuesta ${plan_db.precio_sub}, pero el pago registrado es de solo ${pago_db.monto_membresia}."
        )

    choque_fechas = crud_membresia.verificar_superposicion_fechas(
        db=db, 
        id_cliente=membresia_in.id_cliente, 
        fecha_inicio=membresia_in.fecha_inicio, 
        fecha_fin=membresia_in.fecha_fin
    )
    if choque_fechas:
        raise ConflictException(
            codigo_interno="ERR_CONTRATO_SOLAPADO",
            mensaje=f"El cliente ya tiene una membresía activa en ese rango de fechas (ID Choque: {choque_fechas.id_membresia})."
        )
    return crud_membresia.create(db, obj_in=membresia_in.model_dump())

def obtener_membresias_paginadas(db: Session, page: int, page_size: int, id_cliente: Optional[int] = None, estado: Optional[bool] = None):
    query = crud_membresia.obtener_query_filtrada(db, id_cliente=id_cliente, estado=estado)
    return paginar_resultados(db, crud_membresia, page, page_size, query_personalizada=query)

def actualizar_membresia(db: Session, id_membresia: int, membresia_in: membresia_schema.MembresiaUpdate):
    membresia_actual = crud_membresia.get(db=db, id=id_membresia)
    if not membresia_actual:
        raise NotFoundException(codigo_interno="ERR_NO_ENCONTRADA", mensaje="La membresía solicitada no existe.")

    update_data = membresia_in.model_dump(exclude_unset=True)

    fecha_inic_check = update_data.get("fecha_inicio", membresia_actual.fecha_inicio)
    fecha_fin_check = update_data.get("fecha_fin", membresia_actual.fecha_fin)

    if isinstance(fecha_inic_check, datetime):
        fecha_inic_check = fecha_inic_check.date()
    if isinstance(fecha_fin_check, datetime):
        fecha_fin_check = fecha_fin_check.date()

    update_data["fecha_inicio"] = fecha_inic_check
    update_data["fecha_fin"] = fecha_fin_check

    if fecha_fin_check <= fecha_inic_check:
        raise BadRequestException(
            codigo_interno="ERR_FECHAS_INVALIDAS",
            mensaje="Error de Modificación: La fecha de finalización debe ser estrictamente posterior a su fecha de inicio."
        )

    efectivo_id_cliente = update_data.get("id_cliente", membresia_actual.id_cliente)
    efectivo_id_plan = update_data.get("id_plan", membresia_actual.id_plan)
    efectivo_id_pago = update_data.get("id_pago", membresia_actual.id_pago)

    if not crud_cliente.get(db=db, id=efectivo_id_cliente):
        raise NotFoundException(codigo_interno="ERR_CLIENTE_NOT_FOUND", mensaje="El nuevo cliente ingresado no existe.")
    plan_db = crud_plan.get(db=db, id=efectivo_id_plan)
    if not plan_db:
        raise NotFoundException(codigo_interno="ERR_PLAN_NOT_FOUND", mensaje="El nuevo plan seleccionado no existe.")
    pago_db = crud_pago_membresia.get(db=db, id=efectivo_id_pago)
    if not pago_db:
        raise NotFoundException(codigo_interno="ERR_PAGO_NOT_FOUND", mensaje="El nuevo recibo de pago indicado no existe.")


    if pago_db.id_cliente != efectivo_id_cliente:
        raise ConflictException(
            codigo_interno="ERR_PAGO_AJENO", 
            mensaje="Inconsistencia: El recibo de pago no pertenece al cliente asociado a la membresía."
        )

    membresia_dup = crud_membresia.get_by_pago_id(db=db, id_pago=efectivo_id_pago)
    if membresia_dup and membresia_dup.id_membresia != id_membresia:
        raise ConflictException(
            codigo_interno="ERR_PAGO_YA_UTILIZADO", 
            mensaje="Inconsistencia: El nuevo ID de pago asignado ya está siendo usado por otro contrato."
        )
    if pago_db.monto_membresia < plan_db.precio_sub:
        raise BadRequestException(
            codigo_interno="ERR_FONDOS_INSUFICIENTES", 
            mensaje=f"Error en modificación: El plan cuesta ${plan_db.precio_sub}, pero el pago avala solo ${pago_db.monto_membresia}."
        )
    if "fecha_inicio" in update_data or "fecha_fin" in update_data or "id_cliente" in update_data:
        choque_fechas = crud_membresia.verificar_superposicion_fechas(
            db=db,
            id_cliente=efectivo_id_cliente,
            fecha_inicio=fecha_inic_check,
            fecha_fin=fecha_fin_check,
            id_membresia_excluir=id_membresia
        )
        if choque_fechas:
            raise ConflictException(
                codigo_interno="ERR_CONTRATO_SOLAPADO",
                mensaje=f"No se puede modificar: El nuevo rango interfiere con otra membresía activa del cliente (ID contrato chocante: {choque_fechas.id_membresia})."
            )
    return crud_membresia.update(db=db, db_obj=membresia_actual, obj_in=update_data)
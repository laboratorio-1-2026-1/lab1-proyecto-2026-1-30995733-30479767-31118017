from fastapi import status
from app.core.exceptions import BadRequestException, ConflictException, NotFoundException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from app.core.utils import paginar_resultados
from app.schemas import reserva_schema
from app.repositories.reserva_repository import reserva as crud_reserva
from app.repositories.sesion_repository import sesion as crud_sesion 
from app.repositories.membresia_repository import membresia as crud_membresia 

def crear_reserva(db: Session, reserva_in: reserva_schema.ReservaCreate):

    sesion_destino = crud_sesion.get(db, id=reserva_in.id_sesion)
    if not sesion_destino:
        raise NotFoundException(codigo_interno="ERR_SESION_NO_ENCONTRADA", mensaje="La sesión de clase solicitada no existe.")

    if datetime.now() >= sesion_destino.fecha_inic:
        raise BadRequestException(codigo_interno="ERR_SESION_INICIADA", mensaje="No se pueden realizar reservas para una sesión en curso o finalizada.")

    hoy = datetime.now().date()
    if not crud_membresia.verificar_membresia_activa(db, id_cliente=reserva_in.id_cliente, fecha_referencia=hoy):
        raise ConflictException(codigo_interno="ERR_MEMBRESIA_INACTIVA", mensaje="Acceso denegado: El cliente no posee una membresía activa y vigente.")

    reservas_actuales = crud_reserva.contar_por_sesion(db, id_sesion=reserva_in.id_sesion)
    if reservas_actuales >= sesion_destino.cupos:
        raise ConflictException(codigo_interno="ERR_CLASE_LLENA", mensaje=f"Operación rechazada: La clase ya alcanzó su límite máximo de {sesion_destino.cupos} participantes.")

    reserva_chocante = crud_reserva.verificar_solapamiento(
        db, 
        id_cliente=reserva_in.id_cliente, 
        fecha_inic=sesion_destino.fecha_inic, 
        fecha_fin=sesion_destino.fecha_fin
    )
    if reserva_chocante:
        raise ConflictException(codigo_interno="ERR_RESERVA_SOLAPAMIENTO", mensaje="Conflicto: El cliente ya tiene una reserva activa en este mismo horario.")

    datos_guardar = reserva_in.model_dump()
    datos_guardar["fecha_reserva"] = datetime.now()

    return crud_reserva.create(db, obj_in=datos_guardar)

def obtener_reservas_paginadas(db: Session, page: int, page_size: int, id_cliente: Optional[int] = None, id_sesion: Optional[int] = None):

    query = crud_reserva.obtener_query_filtrada(db, id_cliente=id_cliente, id_sesion=id_sesion)
    return paginar_resultados(db, crud_reserva, page, page_size, query_personalizada=query)

def actualizar_reserva(db: Session, id_reserva: int, reserva_in: reserva_schema.ReservaUpdate):
    reserva_actual = crud_reserva.get(db=db, id=id_reserva)
    if not reserva_actual:
        raise NotFoundException(codigo_interno="ERR_NO_EXISTE", mensaje="Reserva no encontrada.")
        
    if reserva_in.id_sesion:
        sesion_destino = crud_sesion.get(db, id=reserva_in.id_sesion)
        if not sesion_destino:
             raise NotFoundException(codigo_interno="ERR_SESION", mensaje="Nueva sesión no existe.")

        if datetime.now() >= sesion_destino.fecha_inic:
            raise BadRequestException(
                codigo_interno="ERR_SESION_INICIADA", 
                mensaje="No puedes reagendar para una sesión que ya está en curso o finalizada."
            )

        reservas_actuales = crud_reserva.contar_por_sesion(db, id_sesion=reserva_in.id_sesion)
        if reservas_actuales >= sesion_destino.cupos:
            raise ConflictException(codigo_interno="ERR_CLASE_LLENA", mensaje=f"No se puede cambiar la reserva: La nueva clase ya está llena ({sesion_destino.cupos} cupos).")

        reserva_chocante = crud_reserva.verificar_solapamiento(
            db, 
            id_cliente=reserva_actual.id_cliente, 
            fecha_inic=sesion_destino.fecha_inic, 
            fecha_fin=sesion_destino.fecha_fin,
            id_reserva_excluida=id_reserva
        )
        if reserva_chocante:
            raise ConflictException(codigo_interno="ERR_SOLAPAMIENTO", mensaje="Ya tienes otra reserva en el nuevo horario.")

    update_data = reserva_in.model_dump(exclude_unset=True)
    return crud_reserva.update(db=db, db_obj=reserva_actual, obj_in=update_data)
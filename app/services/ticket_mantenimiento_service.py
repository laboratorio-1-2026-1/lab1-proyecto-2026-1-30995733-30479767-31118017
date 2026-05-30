from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from app.core.utils import paginar_resultados
from app.core.exceptions import BadRequestException, NotFoundException, ConflictException
from app.schemas import ticket_mantenimiento_schema
from app.repositories.ticket_mantenimiento_repository import ticket_mantenimiento as crud_ticket_mantenimiento
from app.repositories.maquina_repository import maquina as crud_maquina

def crear_ticket(db: Session, ticket_in: ticket_mantenimiento_schema.TicketMantenimientoCreate):

    maquina_db = crud_maquina.get(db=db, id=ticket_in.id_maquina)
    if not maquina_db:
        raise NotFoundException(
            codigo_interno="ERR_MAQUINA_NO_EXISTE", 
            mensaje="La máquina reportada no existe en el inventario."
        )

    query_abiertos = crud_ticket_mantenimiento.obtener_query_filtrada(db, id_maquina=ticket_in.id_maquina)
    ticket_abierto = query_abiertos.filter(crud_ticket_mantenimiento.model.fecha_resolucion == None).first()
    
    if ticket_abierto:
        raise ConflictException(
            codigo_interno="ERR_TICKET_ABIERTO",
            mensaje=f"La máquina ya posee un ticket de mantenimiento en curso (Ticket #{ticket_abierto.id_ticket})."
        )

    if ticket_in.costo_reparacion is not None and ticket_in.costo_reparacion < 0:
        raise BadRequestException(
            codigo_interno="ERR_COSTO_INVALIDO",
            mensaje="El costo de reparación no puede ser un valor negativo."
        )

    if ticket_in.desc_fallo:
        ticket_in.desc_fallo = ticket_in.desc_fallo.strip()
        if not ticket_in.desc_fallo:
            raise BadRequestException(
                codigo_interno="ERR_DESC_VACIA",
                mensaje="La descripción del fallo no puede estar vacía o contener solo espacios."
            )

    nuevo_estado = "Fuera de Servicio" if "roto" in ticket_in.desc_fallo.lower() else "En Mantenimiento"
    crud_maquina.update(db=db, db_obj=maquina_db, obj_in={"estado_maquina": nuevo_estado})

    if not ticket_in.fecha_falla:
        ticket_in.fecha_falla = datetime.now()
    else:
        ticket_in.fecha_falla = ticket_in.fecha_falla.replace(tzinfo=None)

    return crud_ticket_mantenimiento.create(db, obj_in=ticket_in.model_dump())


def obtener_tickets_paginados(db: Session, page: int, page_size: int, id_maquina: Optional[int] = None):

    query = crud_ticket_mantenimiento.obtener_query_filtrada(db, id_maquina=id_maquina)
    return paginar_resultados(db, crud_ticket_mantenimiento, page, page_size, query_personalizada=query)


def actualizar_estado_ticket(db: Session, id_ticket: int, ticket_in: ticket_mantenimiento_schema.TicketMantenimientoUpdate):

    ticket_actual = crud_ticket_mantenimiento.get(db=db, id=id_ticket)
    if not ticket_actual:
        raise NotFoundException(
            codigo_interno="ERR_TICKET_NO_ENCONTRADO", 
            mensaje="Ticket de mantenimiento no encontrado."
        )

    update_data = ticket_in.model_dump(exclude_unset=True)

    if "costo_reparacion" in update_data and update_data["costo_reparacion"] is not None:
        if update_data["costo_reparacion"] < 0:
            raise BadRequestException(
                codigo_interno="ERR_COSTO_INVALIDO", 
                mensaje="El costo de reparación no puede ser un valor negativo."
            )

    if "desc_fallo" in update_data and update_data["desc_fallo"]:
        update_data["desc_fallo"] = update_data["desc_fallo"].strip()
        if not update_data["desc_fallo"]:
            raise BadRequestException(codigo_interno="ERR_DESC_VACIA", mensaje="La descripción del fallo no puede quedar vacía.")

    fecha_falla_check = ticket_actual.fecha_falla
    if "fecha_resolucion" in update_data and update_data["fecha_resolucion"] is not None:
        update_data["fecha_resolucion"] = update_data["fecha_resolucion"].replace(tzinfo=None)
        if update_data["fecha_resolucion"] < fecha_falla_check:
            raise BadRequestException(
                codigo_interno="ERR_FECHA_RESOLUCION_INVALIDA",
                mensaje="Error de Bitácora: La fecha de resolución no puede ser anterior a la fecha en que se reportó la falla."
            )

    if "fecha_resolucion" in update_data and update_data["fecha_resolucion"] is not None:
        maquina_db = crud_maquina.get(db=db, id=ticket_actual.id_maquina)
        if maquina_db:
            crud_maquina.update(db=db, db_obj=maquina_db, obj_in={"estado_maquina": "Operativa"})

    return crud_ticket_mantenimiento.update(db=db, db_obj=ticket_actual, obj_in=update_data)
from fastapi import status
from app.core.exceptions import BadRequestException, NotFoundException, ConflictException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from app.core.utils import paginar_resultados
from app.schemas import control_acceso_schema
from app.repositories.control_acceso_repository import control_acceso as crud_control_acceso
from app.repositories.cliente_repository import cliente as crud_cliente
from app.repositories.membresia_repository import membresia as crud_membresia

def procesar_entrada_torniquete(db: Session, torniquete_in: control_acceso_schema.TorniqueteInput):

    cedula_limpia = torniquete_in.cedula.strip().upper()
    if not cedula_limpia:
        raise BadRequestException(
            codigo_interno="ERR_CEDULA_VACIA",
            mensaje="Operación rechazada: El código de cédula escaneado no puede estar vacío."
        )

    cliente_db = crud_cliente.get_by_cedula(db, cedula=cedula_limpia)
    if not cliente_db:
        raise NotFoundException(
            codigo_interno="ERR_CEDULA_NO_REGISTRADA",
            mensaje=f"Acceso denegado: La cédula '{cedula_limpia}' no pertenece a ningún cliente activo en el sistema."
        )
    hoy_fecha = datetime.now().date()

    tiene_permiso = crud_membresia.verificar_membresia_activa(
        db, id_cliente=cliente_db.id_cliente, fecha_referencia=hoy_fecha
    )

    if not tiene_permiso:
        raise ConflictException(
            codigo_interno="ERR_MEMBRESIA_VENCIDA",
            mensaje=f"Acceso denegado: El cliente {cliente_db.nombre_cli} {cliente_db.apellido_cli} no posee una membresía activa o su plan ya expiró."
        )

    obj_in = {
        "id_cliente": cliente_db.id_cliente,
        "fecha_entrada": datetime.now()
    }
    return crud_control_acceso.create(db=db, obj_in=obj_in)

def obtener_accesos_paginados(db: Session, page: int, page_size: int, cedula: Optional[str] = None):
    if cedula:
        cedula = cedula.strip().upper()
    query = crud_control_acceso.obtener_query_filtrada(db, cedula=cedula)
    return paginar_resultados(db, crud_control_acceso, page, page_size, query_personalizada=query)
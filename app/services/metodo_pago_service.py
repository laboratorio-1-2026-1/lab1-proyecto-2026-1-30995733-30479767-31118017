from fastapi import status
from app.core.exceptions import BadRequestException, ConflictException, NotFoundException
from sqlalchemy.orm import Session
from typing import Optional
from app.core.utils import paginar_resultados
from app.schemas import metodo_pago_schema
from app.repositories.metodo_pago_repository import metodo_pago as crud_metodo_pago

def crear_metodo_pago(db: Session, metodo_in: metodo_pago_schema.MetodoPagoCreate):

    nombre_limpio = " ".join(metodo_in.nombre_metodo.strip().split()).title()
    
    if not nombre_limpio:
        raise BadRequestException(
            codigo_interno="ERR_DATO_OBLIGATORIO",
            mensaje="El nombre del método de pago es obligatorio y no puede estar vacío."
        )

    if crud_metodo_pago.get_by_nombre(db, nombre_metodo=nombre_limpio):
        raise ConflictException(
            codigo_interno="ERR_METODO_PAGO_DUPLICADO",
            mensaje=f"El método de pago '{nombre_limpio}' ya está registrado en el sistema."
        )
    
    metodo_in.nombre_metodo = nombre_limpio
    return crud_metodo_pago.create(db, obj_in=metodo_in.model_dump())

def obtener_metodos_pago_paginados(db: Session, page: int, page_size: int, nombre_metodo: Optional[str] = None):
    query = crud_metodo_pago.obtener_query_filtrada(db, nombre_metodo=nombre_metodo)
    return paginar_resultados(db, crud_metodo_pago, page, page_size, query_personalizada=query)

def actualizar_metodo_pago(db: Session, id_metodo: int, metodo_in: metodo_pago_schema.MetodoPagoUpdate):
    metodo_actual = crud_metodo_pago.get(db=db, id=id_metodo)
    if not metodo_actual:
        raise NotFoundException(
            codigo_interno="ERR_NO_EXISTE", 
            mensaje="El método de pago solicitado no existe."
        )

    update_data = metodo_in.model_dump(exclude_unset=True)

    if "nombre_metodo" in update_data:
        if update_data["nombre_metodo"] is None:
             raise BadRequestException(codigo_interno="ERR_VACIO", mensaje="El nombre no puede ser nulo.")
             
        nombre_limpio = " ".join(update_data["nombre_metodo"].strip().split()).title()
        
        if not nombre_limpio:
            raise BadRequestException(
                codigo_interno="ERR_VACIO", 
                mensaje="El nombre del método de pago no puede quedar vacío."
            )

        metodo_dup = crud_metodo_pago.get_by_nombre(db, nombre_metodo=nombre_limpio)
        if metodo_dup and metodo_dup.id_metodo != id_metodo:
            raise ConflictException(
                codigo_interno="ERR_DUPLICADO", 
                mensaje=f"No se puede actualizar: El nombre '{nombre_limpio}' ya pertenece a otro método de pago."
            )
            
        update_data["nombre_metodo"] = nombre_limpio

    return crud_metodo_pago.update(db=db, db_obj=metodo_actual, obj_in=update_data)
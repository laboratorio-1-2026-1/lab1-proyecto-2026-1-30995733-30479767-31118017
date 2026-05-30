from fastapi import status
from app.core.exceptions import BadRequestException, NotFoundException, ConflictException
from sqlalchemy.orm import Session
from typing import Optional
from app.core.utils import paginar_resultados
from app.schemas import plan_schema
from app.repositories.plan_repository import plan as crud_plan 

def crear_plan(db: Session, plan_in: plan_schema.PlanCreate):

    nombre_limpio = plan_in.nombre_plan.strip()
    if not nombre_limpio:
        raise BadRequestException(codigo_interno="ERR_NOMBRE_VACIO", mensaje="El nombre del plan no puede estar vacío.")
    
    if crud_plan.get_by_nombre(db, nombre_plan=nombre_limpio):
        raise ConflictException(
            codigo_interno="ERR_PLAN_DUPLICADO", 
            mensaje=f"Ya existe un plan de suscripción registrado con el nombre '{nombre_limpio}'."
        )

    if plan_in.precio_sub <= 0:
        raise BadRequestException(codigo_interno="ERR_PRECIO_INVALIDO", mensaje="El precio del plan debe ser mayor a cero.")
    if plan_in.duracion_dias <= 0 or plan_in.duracion_dias > 3650:
        raise BadRequestException(codigo_interno="ERR_DURACION_INVALIDA", mensaje="La duración del plan debe ser entre 1 y 3650 días (10 años máximos).")

    plan_in.nombre_plan = nombre_limpio
    return crud_plan.create(db, obj_in=plan_in.model_dump())

def obtener_planes_paginados(db: Session, page: int, page_size: int, nombre: Optional[str] = None):
    query = crud_plan.obtener_query_filtrada(db, nombre_plan=nombre)
    return paginar_resultados(db, crud_plan, page, page_size, query_personalizada=query)

def actualizar_plan(db: Session, id_plan: int, plan_in: plan_schema.PlanUpdate):
    plan_actual = crud_plan.get(db=db, id=id_plan)
    if not plan_actual:
        raise NotFoundException(codigo_interno="ERR_PLAN_NO_ENCONTRADO", mensaje=f"No se encontró ningún plan con el ID {id_plan}")

    if plan_in.nombre_plan is not None:
        nombre_limpio = plan_in.nombre_plan.strip()
        if not nombre_limpio:
            raise BadRequestException(codigo_interno="ERR_NOMBRE_VACIO", mensaje="El nombre del plan no puede quedar vacío.")
            
        plan_dup = crud_plan.get_by_nombre(db, nombre_plan=nombre_limpio)
        if plan_dup and plan_dup.id_plan != id_plan:
            raise ConflictException(codigo_interno="ERR_PLAN_DUPLICADO", mensaje=f"El nombre '{nombre_limpio}' ya está siendo usado por otro plan.")
        
        plan_in.nombre_plan = nombre_limpio

    if plan_in.precio_sub is not None and plan_in.precio_sub <= 0:
        raise BadRequestException(codigo_interno="ERR_PRECIO_INVALIDO", mensaje="El precio del plan debe ser mayor a cero.")
    if plan_in.duracion_dias is not None and (plan_in.duracion_dias <= 0 or plan_in.duracion_dias > 3650):
        raise BadRequestException(codigo_interno="ERR_DURACION_INVALIDA", mensaje="La duración del plan debe estar entre 1 y 3650 días.")

    update_data = plan_in.model_dump(exclude_unset=True)
    return crud_plan.update(db=db, db_obj=plan_actual, obj_in=update_data)
from fastapi import status
from app.core.exceptions import BadRequestException, ConflictException, NotFoundException
from sqlalchemy.orm import Session
from typing import Optional
from app.core.utils import paginar_resultados
from app.schemas import rol_schema
from app.repositories.rol_repository import rol as crud_rol

def crear_rol(db: Session, rol_in: rol_schema.RolCreate):

    nombre_limpio = rol_in.nombre_rol.strip().title()
    
    if not nombre_limpio:
        raise BadRequestException(
            codigo_interno="ERR_NOMBRE_VACIO",
            mensaje="El nombre del rol es obligatorio y no puede estar vacío."
        )

    if crud_rol.get_by_nombre(db, nombre_rol=nombre_limpio):
        raise ConflictException(
            codigo_interno="ERR_ROL_DUPLICADO",
            mensaje=f"El rol '{nombre_limpio}' ya se encuentra registrado en el sistema."
        )

    rol_in.nombre_rol = nombre_limpio
    if rol_in.descripcion:
        rol_in.descripcion = rol_in.descripcion.strip()
        
    return crud_rol.create(db, obj_in=rol_in.model_dump())

def obtener_roles_paginados(db: Session, page: int, page_size: int, nombre_filtro: Optional[str] = None):

    query = crud_rol.obtener_query_filtrada(db, nombre_filtro=nombre_filtro)
    return paginar_resultados(db, crud_rol, page, page_size, query_personalizada=query)


def actualizar_rol(db: Session, id_rol: int, rol_in: rol_schema.RolUpdate):

    rol_actual = crud_rol.get(db=db, id=id_rol)
    if not rol_actual:
        raise NotFoundException(codigo_interno="ERR_NO_EXISTE", mensaje="El rol solicitado no existe.")
        
    update_data = rol_in.model_dump(exclude_unset=True)

    if "nombre_rol" in update_data:
        nombre_limpio = update_data["nombre_rol"].strip().title()
        if not nombre_limpio:
            raise BadRequestException(
                codigo_interno="ERR_NOMBRE_VACIO", 
                mensaje="El nombre del rol no puede quedar vacío."
            )

        rol_dup = crud_rol.get_by_nombre(db, nombre_rol=nombre_limpio)
        if rol_dup and rol_dup.id_rol != id_rol:
            raise ConflictException(
                codigo_interno="ERR_ROL_DUPLICADO", 
                mensaje=f"El nombre '{nombre_limpio}' ya pertenece a otro rol registrado."
            )
        update_data["nombre_rol"] = nombre_limpio

    if "descripcion" in update_data and update_data["descripcion"]:
        update_data["descripcion"] = update_data["descripcion"].strip()

    return crud_rol.update(db=db, db_obj=rol_actual, obj_in=update_data)
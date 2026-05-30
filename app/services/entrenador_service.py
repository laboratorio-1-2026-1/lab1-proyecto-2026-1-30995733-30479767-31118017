from fastapi import status
from app.core.exceptions import BadRequestException, ConflictException, NotFoundException
from sqlalchemy.orm import Session
from typing import Optional
from app.core.utils import paginar_resultados
from app.schemas import entrenador_schema
from app.repositories.entrenador_repository import entrenador as crud_entrenador
from app.repositories.usuario_repository import usuario as crud_usuario 

def crear_entrenador(db: Session, entrenador_in: entrenador_schema.EntrenadorCreate):

    nombre_limpio = " ".join(entrenador_in.nombre_ent.strip().split()).title()
    apellido_limpio = " ".join(entrenador_in.apellido_ent.strip().split()).title()
    
    if not nombre_limpio or not apellido_limpio:
        raise BadRequestException(
            codigo_interno="ERR_DATOS_VACIOS",
            mensaje="El nombre y el apellido del entrenador son campos obligatorios."
        )

    usuario_db = crud_usuario.get(db=db, id=entrenador_in.id_usuario)
    if not usuario_db:
        raise NotFoundException(
            codigo_interno="ERR_USUARIO_NO_ENCONTRADO",
            mensaje="El ID de usuario especificado no existe en el sistema."
        )

    if usuario_db.id_rol != 3:
        raise ConflictException(
            codigo_interno="ERR_ROL_INVALIDO",
            mensaje="Incongruencia: La cuenta web especificada no posee el rol de Entrenador (Rol 3)."
        )

    if crud_entrenador.get_by_usuario_id(db=db, id_usuario=entrenador_in.id_usuario):
        raise ConflictException(
            codigo_interno="ERR_PERFIL_DUPLICADO",
            mensaje="Esta cuenta de usuario ya tiene un perfil de entrenador enlazado."
        )

    entrenador_in.nombre_ent = nombre_limpio
    entrenador_in.apellido_ent = apellido_limpio
    
    if entrenador_in.especialidad:
        entrenador_in.especialidad = " ".join(entrenador_in.especialidad.strip().split()).title()

    return crud_entrenador.create(db, obj_in=entrenador_in.model_dump())

def obtener_entrenadores_paginados(db: Session, page: int, page_size: int, especialidad: Optional[str] = None):
    query = crud_entrenador.obtener_query_filtrada(db, especialidad=especialidad)
    return paginar_resultados(db, crud_entrenador, page, page_size, query_personalizada=query)

def actualizar_entrenador(db: Session, id_entrenador: int, entrenador_in: entrenador_schema.EntrenadorUpdate):
    entrenador_actual = crud_entrenador.get(db=db, id=id_entrenador)
    if not entrenador_actual:
        raise NotFoundException(codigo_interno="ERR_NO_EXISTE", mensaje="Entrenador no encontrado en el sistema.")

    update_data = entrenador_in.model_dump(exclude_unset=True)

    if "nombre_ent" in update_data:
        nombre_limpio = " ".join(update_data["nombre_ent"].strip().split()).title()
        if not nombre_limpio:
            raise BadRequestException(codigo_interno="ERR_VACIO", mensaje="El nombre no puede quedar vacío.")
        update_data["nombre_ent"] = nombre_limpio

    if "apellido_ent" in update_data:
        apellido_limpio = " ".join(update_data["apellido_ent"].strip().split()).title()
        if not apellido_limpio:
            raise BadRequestException(codigo_interno="ERR_VACIO", mensaje="El apellido no puede quedar vacío.")
        update_data["apellido_ent"] = apellido_limpio

    if "especialidad" in update_data and update_data["especialidad"] is not None:
        update_data["especialidad"] = " ".join(update_data["especialidad"].strip().split()).title()
        
    if "id_usuario" in update_data and update_data["id_usuario"] != entrenador_actual.id_usuario:
        nuevo_usuario = crud_usuario.get(db=db, id=update_data["id_usuario"])
        if not nuevo_usuario:
            raise NotFoundException(codigo_interno="ERR_USUARIO_NO_ENCONTRADO", mensaje="La nueva cuenta de usuario especificada no existe.")
        if nuevo_usuario.id_rol != 3:
            raise ConflictException(codigo_interno="ERR_ROL_INVALIDO", mensaje="La nueva cuenta no posee el rol de Entrenador.")
        if crud_entrenador.get_by_usuario_id(db=db, id_usuario=update_data["id_usuario"]):
            raise ConflictException(codigo_interno="ERR_PERFIL_DUPLICADO", mensaje="La nueva cuenta ya pertenece a otro entrenador físico.")

    return crud_entrenador.update(db=db, db_obj=entrenador_actual, obj_in=update_data)
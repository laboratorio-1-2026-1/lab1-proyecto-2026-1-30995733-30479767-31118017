from fastapi import status
from app.core.exceptions import BadRequestException, ConflictException, NotFoundException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from app.core.utils import paginar_resultados
from app.schemas import sesion_clase_schema
from app.repositories.sesion_repository import sesion as crud_sesion
from app.repositories.disciplina_repository import disciplina as crud_disciplina
from app.repositories.entrenador_repository import entrenador as crud_entrenador

def crear_sesion(db: Session, sesion_in: sesion_clase_schema.SesionClaseCreate):

    inicio_real = sesion_in.fecha_inic.replace(tzinfo=None)
    fin_real = sesion_in.fecha_fin.replace(tzinfo=None)

    if inicio_real >= fin_real:
        raise BadRequestException(
            codigo_interno="ERR_FECHAS_INVALIDAS", 
            mensaje="Error de Cronograma: La fecha y hora de inicio debe ser estrictamente anterior a la de finalización."
        )
        
    if inicio_real < datetime.now():
        raise BadRequestException(
            codigo_interno="ERR_FECHA_PASADA",
            mensaje="Operación rechazada: No se pueden programar sesiones de clase en el pasado."
        )

    if sesion_in.cupos <= 0 or sesion_in.cupos > 100:
        raise BadRequestException(
            codigo_interno="ERR_CUPOS_INVALIDOS", 
            mensaje="El número de cupos asignados debe ser un valor estimado real entre 1 y 100 participantes máximos por clase."
        )

    if not crud_disciplina.get(db=db, id=sesion_in.id_disciplina):
        raise NotFoundException(
            codigo_interno="ERR_DISCIPLINA_NOT_FOUND",
            mensaje="La disciplina (ej. Yoga, CrossFit) seleccionada para esta sesión no existe en el catálogo."
        )

    if not crud_entrenador.get(db=db, id=sesion_in.id_entrenador):
        raise NotFoundException(
            codigo_interno="ERR_ENTRENADOR_NOT_FOUND",
            mensaje="El entrenador asignado para dirigir esta clase no está registrado en el sistema."
        )

    choque = crud_sesion.verificar_choque_entrenador(
        db=db, id_entrenador=sesion_in.id_entrenador, inicio=inicio_real, fin=fin_real
    )
    if choque:
        raise ConflictException(
            codigo_interno="ERR_ENTRENADOR_OCUPADO",
            mensaje=f"Conflicto de Agenda: El entrenador ya se encuentra asignado a otra sesión en ese mismo horario (ID de clase chocante: {choque.id_sesion})."
        )

    sesion_in.fecha_inic = inicio_real
    sesion_in.fecha_fin = fin_real
    return crud_sesion.create(db, obj_in=sesion_in.model_dump())


def obtener_sesiones_paginadas(
    db: Session, page: int, page_size: int, id_disciplina: Optional[int] = None, id_entrenador: Optional[int] = None
):

    query = crud_sesion.obtener_query_filtrada(db, id_disciplina=id_disciplina, id_entrenador=id_entrenador)
    return paginar_resultados(db, crud_sesion, page, page_size, query_personalizada=query)


def actualizar_sesion(db: Session, id_sesion: int, sesion_in: sesion_clase_schema.SesionClaseUpdate):

    sesion_actual = crud_sesion.get(db=db, id=id_sesion)
    if not sesion_actual:
        raise NotFoundException(
            codigo_interno="ERR_NO_EXISTE", 
            mensaje="La sesión de clase solicitada para modificación no existe."
        )

    inicio_check = sesion_in.fecha_inic.replace(tzinfo=None) if sesion_in.fecha_inic else sesion_actual.fecha_inic
    fin_check = sesion_in.fecha_fin.replace(tzinfo=None) if sesion_in.fecha_fin else sesion_actual.fecha_fin
    entrenador_check = sesion_in.id_entrenador if sesion_in.id_entrenador else sesion_actual.id_entrenador

    if inicio_check >= fin_check:
        raise BadRequestException(
            codigo_interno="ERR_FECHAS_INVALIDAS", 
            mensaje="Error de Modificación: El nuevo horario de inicio debe ser anterior al de finalización."
        )

    if sesion_in.cupos is not None and (sesion_in.cupos <= 0 or sesion_in.cupos > 100):
        raise BadRequestException(
            codigo_interno="ERR_CUPOS_INVALIDOS", 
            mensaje="El número de cupos modificado debe estar en el rango permitido de 1 a 100."
        )

    if sesion_in.id_disciplina and not crud_disciplina.get(db=db, id=sesion_in.id_disciplina):
        raise NotFoundException(codigo_interno="ERR_DISCIPLINA_NOT_FOUND", mensaje="La nueva disciplina asignada no existe.")

    if sesion_in.id_entrenador and not crud_entrenador.get(db=db, id=sesion_in.id_entrenador):
        raise NotFoundException(codigo_interno="ERR_ENTRENADOR_NOT_FOUND", mensaje="El nuevo entrenador asignado no existe.")

    if sesion_in.fecha_inic or sesion_in.fecha_fin or sesion_in.id_entrenador:
        choque = crud_sesion.verificar_choque_entrenador(
            db=db, id_entrenador=entrenador_check, inicio=inicio_check, fin=fin_check, id_sesion_excluir=id_sesion
        )
        if choque:
            raise ConflictException(
                codigo_interno="ERR_ENTRENADOR_OCUPADO",
                mensaje=f"No se puede reagendar: El entrenador seleccionado interfiere con otra de sus clases (ID conflicto: {choque.id_sesion})."
            )

    update_data = sesion_in.model_dump(exclude_unset=True)

    if "fecha_inic" in update_data:
        update_data["fecha_inic"] = inicio_check
    if "fecha_fin" in update_data:
        update_data["fecha_fin"] = fin_check

    return crud_sesion.update(db=db, db_obj=sesion_actual, obj_in=update_data)
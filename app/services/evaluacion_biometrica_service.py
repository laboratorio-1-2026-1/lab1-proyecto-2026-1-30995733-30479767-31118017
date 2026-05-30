from sqlalchemy.orm import Session
from typing import Optional
from app.core.utils import paginar_resultados
from app.core.exceptions import BadRequestException, NotFoundException
from app.schemas import evaluacion_biometrica_schema
from app.repositories.evaluacion_repository import evaluacion as crud_evaluacion
from app.repositories.cliente_repository import cliente as crud_cliente
from app.repositories.entrenador_repository import entrenador as crud_entrenador

def validar_metricas_biometricas(peso: Optional[float], altura: Optional[float], porc_grasa: Optional[float]):

    if peso is not None and (peso <= 0 or peso > 500):
        raise BadRequestException(
            codigo_interno="ERR_PESO_INVALIDO", 
            mensaje="El peso registrado debe ser mayor a 0 y menor a 500 kg."
        )
    if altura is not None and (altura <= 0 or altura > 3.0):
        raise BadRequestException(
            codigo_interno="ERR_ALTURA_INVALIDA", 
            mensaje="La altura debe ser expresada en metros estrictamente mayores a cero (ej: 1.75)."
        )
    if porc_grasa is not None and (porc_grasa <= 0 or porc_grasa > 100):
        raise BadRequestException(
            codigo_interno="ERR_GRASA_INVALIDA", 
            mensaje="El porcentaje de masa grasa estimado debe estar en el rango de 0.1% a 100%."
        )

def crear_evaluacion(db: Session, eval_in: evaluacion_biometrica_schema.EvaluacionBiometricaCreate):

    validar_metricas_biometricas(eval_in.peso, eval_in.altura, eval_in.porc_grasa)

    if not crud_cliente.get(db=db, id=eval_in.id_cliente):
        raise NotFoundException(
            codigo_interno="ERR_CLIENTE_NO_EXISTE", 
            mensaje="Operación rechazada: El cliente asignado para la evaluación no existe en el sistema."
        )

    if not crud_entrenador.get(db=db, id=eval_in.id_entrenador):
        raise NotFoundException(
            codigo_interno="ERR_ENTRENADOR_NO_EXISTE", 
            mensaje="Operación rechazada: El entrenador firmante de esta evaluación biométrica no existe."
        )

    if eval_in.observaciones:
        eval_in.observaciones = eval_in.observaciones.strip()
    if eval_in.historial:
        eval_in.historial = eval_in.historial.strip()

    return crud_evaluacion.create(db, obj_in=eval_in.model_dump())

def obtener_evaluaciones_paginadas(
    db: Session, page: int, page_size: int, id_cliente: Optional[int] = None, orden_fecha: str = "desc"
):

    query = crud_evaluacion.obtener_query_filtrada(db, id_cliente=id_cliente, orden_fecha=orden_fecha)
    return paginar_resultados(db, crud_evaluacion, page, page_size, query_personalizada=query)

def actualizar_evaluacion(db: Session, id_evaluacion: int, eval_in: evaluacion_biometrica_schema.EvaluacionBiometricaUpdate):

    eval_actual = crud_evaluacion.get(db=db, id=id_evaluacion)
    if not eval_actual:
        raise NotFoundException(
            codigo_interno="ERR_NO_EXISTE", 
            mensaje="La ficha de evaluación biométrica solicitada no existe."
        )
    update_data = eval_in.model_dump(exclude_unset=True)

    peso_chk = update_data.get("peso")
    altura_chk = update_data.get("altura")
    grasa_chk = update_data.get("porc_grasa")

    validar_metricas_biometricas(peso_chk, altura_chk, grasa_chk)

    if "observaciones" in update_data and update_data["observaciones"]:
        update_data["observaciones"] = update_data["observaciones"].strip()
    if "historial" in update_data and update_data["historial"]:
        update_data["historial"] = update_data["historial"].strip()
        
    return crud_evaluacion.update(db=db, db_obj=eval_actual, obj_in=update_data)
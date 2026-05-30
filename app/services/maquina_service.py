from sqlalchemy.orm import Session
from typing import Optional
from app.core.utils import paginar_resultados
from app.core.exceptions import BadRequestException, NotFoundException
from app.schemas import maquina_schema
from app.repositories.maquina_repository import maquina as crud_maquina
from app.repositories.categoria_repository import categoria as crud_categoria

def validar_estado_estricto(estado: str):

    estados_permitidos = ["Operativa", "En Mantenimiento", "Fuera de Servicio"]

    if estado and estado.strip().title() not in estados_permitidos:
        raise BadRequestException(
            codigo_interno="ERR_ESTADO_MAQUINA_INVALIDO",
            mensaje=f"El estado '{estado}' es inválido. Los únicos estados permitidos son: Operativa, En Mantenimiento o Fuera de Servicio."
        )

def crear_maquina(db: Session, maquina_in: maquina_schema.MaquinaCreate):

    nombre_limpio = " ".join(maquina_in.nombre.strip().split()).title()
    if not nombre_limpio:
        raise BadRequestException(
            codigo_interno="ERR_NOMBRE_VACIO", 
            mensaje="El nombre de la máquina es obligatorio y no puede contener solo espacios en blanco."
        )

    if not crud_categoria.get(db=db, id=maquina_in.id_categoria):
        raise NotFoundException(
            codigo_interno="ERR_CATEGORIA_NO_ENCONTRADA", 
            mensaje=f"La categoría de máquina con ID {maquina_in.id_categoria} no existe."
        )

    if maquina_in.estado_maquina:
        validar_estado_estricto(maquina_in.estado_maquina)
        maquina_in.estado_maquina = maquina_in.estado_maquina.strip().title()
    else:
        maquina_in.estado_maquina = "Operativa" 
        
    maquina_in.nombre = nombre_limpio
    return crud_maquina.create(db, obj_in=maquina_in.model_dump())

def obtener_maquinas_paginadas(db: Session, page: int, page_size: int, estado: Optional[str] = None, id_cat: Optional[int] = None):
    query = crud_maquina.obtener_query_filtrada(db, estado=estado, id_cat=id_cat)
    return paginar_resultados(db, crud_maquina, page, page_size, query_personalizada=query)

def actualizar_maquina(db: Session, id_maquina: int, maquina_in: maquina_schema.MaquinaUpdate):
    maquina_actual = crud_maquina.get(db=db, id=id_maquina)
    if not maquina_actual:
        raise NotFoundException(
            codigo_interno="ERR_NO_ENCONTRADA", 
            mensaje=f"Error: No se encontró ninguna máquina con el ID {id_maquina}."
        )

    if maquina_in.estado_maquina:
        validar_estado_estricto(maquina_in.estado_maquina)
        maquina_in.estado_maquina = maquina_in.estado_maquina.strip().title()
        
    if maquina_in.nombre is not None:
        nombre_limpio = " ".join(maquina_in.nombre.strip().split()).title()
        if not nombre_limpio:
            raise BadRequestException(
                codigo_interno="ERR_NOMBRE_VACIO", 
                mensaje="El nombre de la máquina no puede quedar vacío al actualizar."
            )
        maquina_in.nombre = nombre_limpio
        
    if maquina_in.id_categoria is not None:
        if not crud_categoria.get(db=db, id=maquina_in.id_categoria):
            raise NotFoundException(
                codigo_interno="ERR_CATEGORIA_NO_ENCONTRADA", 
                mensaje=f"No se puede actualizar: La categoría con ID {maquina_in.id_categoria} no existe."
            )
        
    update_data = maquina_in.model_dump(exclude_unset=True)
    return crud_maquina.update(db=db, db_obj=maquina_actual, obj_in=update_data)
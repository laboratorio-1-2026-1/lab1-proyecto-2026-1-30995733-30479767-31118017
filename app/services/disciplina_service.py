from sqlalchemy.orm import Session
from typing import Optional
from app.core.exceptions import BadRequestException, ConflictException, NotFoundException 
from app.core.utils import paginar_resultados
from app.schemas import disciplina_schema
from app.repositories.disciplina_repository import disciplina as crud_disciplina

def crear_disciplina(db: Session, disciplina_in: disciplina_schema.DisciplinaCreate):

    nombre_limpio = " ".join(disciplina_in.nombre_disc.strip().split()).title()
    
    if not nombre_limpio:
        raise BadRequestException(
            codigo_interno="ERR_CAMPO_VACIO",
            mensaje="El nombre de la disciplina no puede estar vacío."
        )
        
    if nombre_limpio.isdigit():
        raise BadRequestException(
            codigo_interno="ERR_NOMBRE_INVALIDO",
            mensaje="El nombre de la disciplina debe contener caracteres alfabéticos, no puede ser puramente numérico."
        )

    if crud_disciplina.get_by_nombre(db, nombre_disc=nombre_limpio):
        raise ConflictException(
            codigo_interno="ERR_DISCIPLINA_DUPLICADA",
            mensaje=f"Regla de Negocio: Ya existe una disciplina registrada con el nombre '{nombre_limpio}'."
        )
    disciplina_in.nombre_disc = nombre_limpio

    if hasattr(disciplina_in, 'descripcion') and disciplina_in.descripcion:
        disciplina_in.descripcion = disciplina_in.descripcion.strip()
        
    return crud_disciplina.create(db, obj_in=disciplina_in.model_dump())

def obtener_disciplinas_paginadas(db: Session, page: int, page_size: int, nombre: Optional[str] = None):
    query = crud_disciplina.obtener_query_filtrada(db, nombre_filtro=nombre)
    return paginar_resultados(db, crud_disciplina, page, page_size, query_personalizada=query)


def actualizar_disciplina(db: Session, id_disciplina: int, disciplina_in: disciplina_schema.DisciplinaUpdate):

    disciplina_actual = crud_disciplina.get(db=db, id=id_disciplina)
    if not disciplina_actual:
        raise NotFoundException(
            codigo_interno="ERR_NO_EXISTE", 
            mensaje="La disciplina solicitada no existe en el catálogo."
        )
        
    update_data = disciplina_in.model_dump(exclude_unset=True)

    if "nombre_disc" in update_data:
        nombre_limpio = " ".join(update_data["nombre_disc"].strip().split()).title()
        
        if not nombre_limpio:
            raise BadRequestException(
                codigo_interno="ERR_VACIO", 
                mensaje="El nombre de la disciplina no puede quedar vacío al actualizar."
            )
            
        if nombre_limpio.isdigit():
            raise BadRequestException(
                codigo_interno="ERR_NOMBRE_INVALIDO",
                mensaje="El nombre de la disciplina no puede ser puramente numérico."
            )

        disc_dup = crud_disciplina.get_by_nombre(db, nombre_disc=nombre_limpio)
        if disc_dup and disc_dup.id_disciplina != id_disciplina:
            raise ConflictException(
                codigo_interno="ERR_DUPLICADO", 
                mensaje=f"Inconsistencia: El nombre '{nombre_limpio}' ya está asignado a otra disciplina."
            )
            
        update_data["nombre_disc"] = nombre_limpio

    if "descripcion" in update_data and update_data["descripcion"] is not None:
        update_data["descripcion"] = update_data["descripcion"].strip()

    return crud_disciplina.update(db=db, db_obj=disciplina_actual, obj_in=update_data)
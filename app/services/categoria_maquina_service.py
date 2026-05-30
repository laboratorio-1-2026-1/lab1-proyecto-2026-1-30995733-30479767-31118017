from fastapi import status
from app.core.exceptions import BadRequestException, ConflictException, NotFoundException
from sqlalchemy.orm import Session
from typing import Optional
from app.core.utils import paginar_resultados
from app.schemas import categoria_maquina_schema
from app.repositories.categoria_repository import categoria as crud_categoria

def crear_categoria(db: Session, obj_in: categoria_maquina_schema.CategoriaMaquinaCreate):

    nombre_limpio = " ".join(obj_in.nombre_categoria.strip().split()).title()

    if not nombre_limpio:
        raise BadRequestException(
            codigo_interno="ERR_CAMPO_VACIO",
            mensaje="El nombre de la categoría de máquina es obligatorio y no puede estar vacío."
        )

    if crud_categoria.get_by_nombre(db, nombre_categoria=nombre_limpio):
        raise ConflictException(
            codigo_interno="ERR_CATEGORIA_DUPLICADA",
            mensaje=f"Ya existe una categoría registrada con el nombre '{nombre_limpio}'."
        )

    obj_in.nombre_categoria = nombre_limpio
    return crud_categoria.create(db, obj_in=obj_in.model_dump())

def obtener_categorias_paginadas(db: Session, page: int, page_size: int, nombre_filtro: Optional[str] = None):
    query = crud_categoria.obtener_query_filtrada(db, nombre_filtro=nombre_filtro)
    return paginar_resultados(db, crud_categoria, page, page_size, query_personalizada=query)

def actualizar_categoria(db: Session, id_categoria: int, categoria_in: categoria_maquina_schema.CategoriaMaquinaUpdate):
    categoria_actual = crud_categoria.get(db=db, id=id_categoria)
    if not categoria_actual:
        raise NotFoundException(
            codigo_interno="ERR_NO_EXISTE", 
            mensaje=f"No se encontró ninguna categoría con el ID {id_categoria}."
        )        
    update_data = categoria_in.model_dump(exclude_unset=True)

    if "nombre_categoria" in update_data:
        nombre_limpio = " ".join(update_data["nombre_categoria"].strip().split()).title()
        
        if not nombre_limpio:
            raise BadRequestException(
                codigo_interno="ERR_NOMBRE_VACIO", 
                mensaje="El nombre de la categoría no puede quedar vacío tras la actualización."
            )

        cat_dup = crud_categoria.get_by_nombre(db, nombre_categoria=nombre_limpio)
        if cat_dup and cat_dup.id_categoria != id_categoria:
            raise ConflictException(
                codigo_interno="ERR_DUPLICADA", 
                mensaje=f"El nombre '{nombre_limpio}' ya pertenece a otra categoría en el sistema."
            )
        update_data["nombre_categoria"] = nombre_limpio
    return crud_categoria.update(db=db, db_obj=categoria_actual, obj_in=update_data)
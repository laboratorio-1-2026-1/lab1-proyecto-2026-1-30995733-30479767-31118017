from fastapi import status
from app.core.exceptions import BadRequestException, ConflictException, NotFoundException
from sqlalchemy.orm import Session
from typing import Optional
from app.core.utils import paginar_resultados
from app.schemas import producto_schema
from app.repositories.producto_repository import producto as crud_producto

def crear_producto(db: Session, producto_in: producto_schema.ProductoCreate):

    nombre_limpio = " ".join(producto_in.nombre_prod.strip().split()).title()
    if not nombre_limpio:
        raise BadRequestException(
            codigo_interno="ERR_NOMBRE_VACIO", 
            mensaje="El nombre del producto no puede estar vacío."
        )

    if crud_producto.get_by_nombre(db, nombre_prod=nombre_limpio):
        raise ConflictException(
            codigo_interno="ERR_PRODUCTO_DUPLICADO",
            mensaje=f"El producto '{nombre_limpio}' ya se encuentra registrado en el inventario."
        )

    if producto_in.precio <= 0:
        raise BadRequestException(
            codigo_interno="ERR_PRECIO_INVALIDO", 
            mensaje="El precio del producto debe ser estrictamente mayor a cero."
        )
    if producto_in.stock < 0:
        raise BadRequestException(
            codigo_interno="ERR_STOCK_INVALIDO", 
            mensaje="El stock inicial del producto no puede ser un valor negativo."
        )

    producto_in.nombre_prod = nombre_limpio

    if hasattr(producto_in, 'descripcion_prod') and producto_in.descripcion_prod:
        producto_in.descripcion_prod = producto_in.descripcion_prod.strip()
    return crud_producto.create(db, obj_in=producto_in.model_dump())

def obtener_productos_paginados(db: Session, page: int, page_size: int, nombre: Optional[str] = None):
    query = crud_producto.obtener_query_filtrada(db, nombre_filtro=nombre)
    return paginar_resultados(db, crud_producto, page, page_size, query_personalizada=query)

def actualizar_producto(db: Session, id_producto: int, producto_in: producto_schema.ProductoUpdate):

    producto_actual = crud_producto.get(db=db, id=id_producto)
    if not producto_actual:
        raise NotFoundException(codigo_interno="ERR_NO_EXISTE", mensaje="El producto solicitado no existe.")
    update_data = producto_in.model_dump(exclude_unset=True)

    if "nombre_prod" in update_data:
        nombre_limpio = " ".join(update_data["nombre_prod"].strip().split()).title()
        if not nombre_limpio:
            raise BadRequestException(codigo_interno="ERR_NOMBRE_VACIO", mensaje="El nombre del producto no puede quedar vacío.")

        prod_dup = crud_producto.get_by_nombre(db, nombre_prod=nombre_limpio)
        if prod_dup and prod_dup.id_producto != id_producto:
            raise ConflictException(
                codigo_interno="ERR_PRODUCTO_DUPLICADO", 
                mensaje=f"No se puede renombrar: El nombre '{nombre_limpio}' ya pertenece a otro artículo."
            )
        update_data["nombre_prod"] = nombre_limpio

    if "descripcion_prod" in update_data and update_data["descripcion_prod"] is not None:
        update_data["descripcion_prod"] = update_data["descripcion_prod"].strip()
    if "precio" in update_data and update_data["precio"] <= 0:
        raise BadRequestException(codigo_interno="ERR_PRECIO_INVALIDO", mensaje="El precio modificado debe ser estrictamente mayor a cero.")
    if "stock" in update_data and update_data["stock"] < 0:
        raise BadRequestException(codigo_interno="ERR_STOCK_INVALIDO", mensaje="El stock del inventario no puede quedar en un valor negativo.")
    
    return crud_producto.update(db=db, db_obj=producto_actual, obj_in=update_data)
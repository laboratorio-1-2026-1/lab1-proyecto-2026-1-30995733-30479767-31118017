from pydantic import BaseModel
from typing import List
from app.schemas.paginacion_schema import PaginatedMeta # <-- Cambiado al global

class ProductoBase(BaseModel):
    nombre_prod: str
    precio: float
    stock: int

class ProductoCreate(ProductoBase):
    pass

class ProductoResponse(ProductoBase):
    id_producto: int 

    class Config:
        from_attributes = True

class ProductoPaginatedResponse(BaseModel):
    meta: PaginatedMeta
    rows: List[ProductoResponse]
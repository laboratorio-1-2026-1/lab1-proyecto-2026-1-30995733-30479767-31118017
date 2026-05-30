from pydantic import BaseModel, Field
from typing import List, Optional
from app.schemas.paginacion_schema import PaginatedMeta
from typing import Optional

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

class ProductoUpdate(BaseModel):
    nombre_prod: Optional[str] = None
    precio: Optional[float] = Field(default=None, gt=0)
    stock: Optional[int] = Field(default=None, ge=0)

class ProductoPaginatedResponse(BaseModel):
    meta: PaginatedMeta
    rows: List[ProductoResponse]
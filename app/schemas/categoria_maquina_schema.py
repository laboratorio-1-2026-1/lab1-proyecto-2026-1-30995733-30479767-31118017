from pydantic import BaseModel
from typing import List
from app.schemas.paginacion_schema import PaginatedMeta

class CategoriaMaquinaBase(BaseModel):
    nombre_categoria: str

class CategoriaMaquinaCreate(CategoriaMaquinaBase):
    pass

class CategoriaMaquinaResponse(CategoriaMaquinaBase):
    id_categoria: int

    class Config:
        from_attributes = True


class CategoriaMaquinaPaginatedResponse(BaseModel):
    meta: PaginatedMeta
    rows: List[CategoriaMaquinaResponse]
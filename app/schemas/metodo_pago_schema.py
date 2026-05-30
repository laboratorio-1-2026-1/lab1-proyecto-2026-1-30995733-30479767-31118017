from pydantic import BaseModel
from typing import List, Optional
from app.schemas.paginacion_schema import PaginatedMeta

class MetodoPagoBase(BaseModel):
    nombre_metodo: str

class MetodoPagoCreate(MetodoPagoBase):
    pass

class MetodoPagoResponse(MetodoPagoBase):
    id_metodo: int

    class Config:
        from_attributes = True

class MetodoPagoUpdate(BaseModel):
    nombre_metodo: Optional[str] = None

class MetodoPagoPaginatedResponse(BaseModel):
    meta: PaginatedMeta
    rows: List[MetodoPagoResponse]
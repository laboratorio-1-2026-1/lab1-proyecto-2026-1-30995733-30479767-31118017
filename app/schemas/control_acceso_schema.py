from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.schemas.paginacion_schema import PaginatedMeta

class ControlAccesoBase(BaseModel):
    id_cliente: int
    fecha_entrada: Optional[datetime] = None

class ControlAccesoCreate(ControlAccesoBase):
    pass

class ControlAccesoResponse(ControlAccesoBase):
    id_acceso: int

    class Config:
        from_attributes = True


class ControlAccesoPaginatedResponse(BaseModel):
    meta: PaginatedMeta
    rows: List[ControlAccesoResponse]
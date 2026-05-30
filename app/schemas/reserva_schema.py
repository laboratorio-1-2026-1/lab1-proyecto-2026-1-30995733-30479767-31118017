from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from app.schemas.paginacion_schema import PaginatedMeta

class ReservaBase(BaseModel):
    id_cliente: int
    id_sesion: int
    fecha_reserva: datetime

class ReservaCreate(ReservaBase):
    pass

class ReservaResponse(ReservaBase):
    id_reserva: int

    class Config:
        from_attributes = True

class ReservaUpdate(BaseModel):
    id_sesion: Optional[int] = None

class ReservaPaginatedResponse(BaseModel):
    meta: PaginatedMeta
    rows: List[ReservaResponse]
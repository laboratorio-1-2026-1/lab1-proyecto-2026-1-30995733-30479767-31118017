from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from app.schemas.paginacion_schema import PaginatedMeta

class ReservaCreate(BaseModel):
    id_cliente: int = Field(..., gt=0)
    id_sesion: int = Field(..., gt=0)

class ReservaResponse(ReservaCreate):
    id_reserva: int
    fecha_reserva: datetime = Field(description="Timestamp automático de la transacción")

    class Config:
        from_attributes = True

class ReservaUpdate(BaseModel):
    id_sesion: Optional[int] = None

class ReservaPaginatedResponse(BaseModel):
    meta: PaginatedMeta
    rows: List[ReservaResponse]
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from app.schemas.paginacion_schema import PaginatedMeta

class ControlAccesoBase(BaseModel):
    id_cliente: int
    fecha_entrada: Optional[datetime] = None

class TorniqueteInput(BaseModel):
    cedula: str = Field(..., min_length=5, description="Número de cédula escaneado en la puerta")

class ControlAccesoCreate(ControlAccesoBase):
    pass

class ControlAccesoResponse(ControlAccesoBase):
    id_acceso: int

    class Config:
        from_attributes = True

class ControlAccesoPaginatedResponse(BaseModel):
    meta: PaginatedMeta
    rows: List[ControlAccesoResponse]
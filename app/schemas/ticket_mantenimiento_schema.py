from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.schemas.paginacion_schema import PaginatedMeta

class TicketMantenimientoBase(BaseModel):
    id_maquina: int
    desc_fallo: str
    costo_reparacion: Optional[float] = None
    fecha_falla: Optional[datetime] = None
    fecha_resolucion: Optional[datetime] = None

class TicketMantenimientoCreate(TicketMantenimientoBase):
    pass

class TicketMantenimientoResponse(TicketMantenimientoBase):
    id_ticket: int 

    class Config:
        from_attributes = True

class TicketMantenimientoUpdate(BaseModel):
    id_maquina: Optional[int] = None
    desc_fallo: Optional[str] = None
    costo_reparacion: Optional[float] = None
    fecha_falla: Optional[datetime] = None
    fecha_resolucion: Optional[datetime] = None


class TicketMantenimientoPaginatedResponse(BaseModel):
    meta: PaginatedMeta
    rows: List[TicketMantenimientoResponse]
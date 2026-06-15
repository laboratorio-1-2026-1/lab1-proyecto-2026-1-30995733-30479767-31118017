from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from app.schemas.paginacion_schema import PaginatedMeta

class TicketMantenimientoCreate(BaseModel):
    id_maquina: int = Field(..., gt=0)
    desc_fallo: str = Field(..., min_length=0)
    costo_reparacion: Optional[float] = Field(default=None)

class TicketMantenimientoResponse(TicketMantenimientoCreate):
    id_ticket: int 
    fecha_falla: datetime = Field(description="Registrado automáticamente al crear")
    fecha_resolucion: Optional[datetime] = Field(default=None, description="Registrado al cerrar el ticket")

    class Config:
        from_attributes = True

class TicketMantenimientoUpdate(BaseModel):
    desc_fallo: Optional[str] = None
    costo_reparacion: Optional[float] = Field(default=None)
    fecha_resolucion: Optional[datetime] = None

class TicketMantenimientoPaginatedResponse(BaseModel):
    meta: PaginatedMeta
    rows: List[TicketMantenimientoResponse]
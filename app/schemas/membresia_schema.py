from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List
from app.schemas.paginacion_schema import PaginatedMeta

class MembresiaBase(BaseModel):
    id_cliente: int = Field(..., gt=0)
    id_plan: int = Field(..., gt=0)
    id_pago: int = Field(..., gt=0) 
    fecha_inicio: date
    fecha_fin: date
    estado: Optional[bool] = Field(default=True, description="True = Activa, False = Suspendida Manualmente")

class MembresiaCreate(MembresiaBase):
    pass

class MembresiaResponse(MembresiaBase):
    id_membresia: int
    estado_dinamico: Optional[str] = Field(default=None, description="Calculado en tiempo real")

    class Config:
        from_attributes = True

class MembresiaUpdate(BaseModel):
    id_plan: Optional[int] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    estado: Optional[bool] = None

class MembresiaPaginatedResponse(BaseModel):
    meta: PaginatedMeta
    rows: List[MembresiaResponse]
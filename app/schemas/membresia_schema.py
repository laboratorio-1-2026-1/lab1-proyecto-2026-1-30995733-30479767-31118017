from pydantic import BaseModel
from datetime import date
from typing import Optional, List
from app.schemas.paginacion_schema import PaginatedMeta

class MembresiaBase(BaseModel):
    id_cliente: int
    id_plan: int
    id_pago: int 
    fecha_inicio: date
    fecha_fin: date
    estado: Optional[str] = "Activa"

class MembresiaCreate(MembresiaBase):
    pass

class MembresiaResponse(MembresiaBase):
    id_membresia: int

    class Config:
        from_attributes = True


class MembresiaPaginatedResponse(BaseModel):
    meta: PaginatedMeta
    rows: List[MembresiaResponse]
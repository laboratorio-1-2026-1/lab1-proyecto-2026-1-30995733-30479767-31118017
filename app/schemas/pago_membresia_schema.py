from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.schemas.paginacion_schema import PaginatedMeta

class PagoMembresiaBase(BaseModel):
    id_cliente: int
    id_metodo: int
    monto_membresia: float
    referencia: Optional[str] = None
    fecha_pago: datetime
    estado_pago: Optional[str] = "Completado"

class PagoMembresiaCreate(PagoMembresiaBase):
    pass

class PagoMembresiaResponse(PagoMembresiaBase):
    id_pago: int

    class Config:
        from_attributes = True

class PagoMembresiaPaginatedResponse(BaseModel):
    meta: PaginatedMeta
    rows: List[PagoMembresiaResponse]
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from app.schemas.paginacion_schema import PaginatedMeta

class PagoMembresiaBase(BaseModel):
    id_cliente: int = Field(..., gt=0)
    id_metodo: int = Field(..., gt=0)
    monto_membresia: float = Field(..., gt=0)
    referencia: Optional[str] = Field(default=None, max_length=100)

class PagoMembresiaCreate(PagoMembresiaBase):
    pass

class PagoMembresiaResponse(PagoMembresiaBase):
    id_pago: int
    fecha_pago: datetime = Field(description="Generada automáticamente por la BD")
    estado_pago: str = Field(description="Siempre será Completado")

    class Config:
        from_attributes = True

class PagoMembresiaPaginatedResponse(BaseModel):
    meta: PaginatedMeta
    rows: List[PagoMembresiaResponse]
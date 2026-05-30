from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from app.schemas.paginacion_schema import PaginatedMeta

class VentaProductoCreate(BaseModel):
    id_cliente: int = Field(..., gt=0)
    id_metodo: int = Field(..., gt=0)
    referencia: Optional[str] = Field(default=None, max_length=100)

class VentaProductoResponse(VentaProductoCreate):
    id_venta: int
    fecha_venta: datetime
    monto_total: float = Field(description="Suma automática de los subtotales")
    estado_venta: str = Field(description="Estado inmutable de la factura")

    class Config:
        from_attributes = True

class VentaProductoPaginatedResponse(BaseModel):
    meta: PaginatedMeta
    rows: List[VentaProductoResponse]
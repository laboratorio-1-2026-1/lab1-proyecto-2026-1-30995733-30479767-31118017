from pydantic import BaseModel, Field
from typing import List
from app.schemas.paginacion_schema import PaginatedMeta

class RegistroVentaCreate(BaseModel):
    id_venta: int = Field(..., gt=0, description="ID de la factura principal")
    id_producto: int = Field(..., gt=0, description="ID del producto a comprar")
    cantidad: int = Field(..., gt=0, description="Cantidad de unidades")

class RegistroVentaResponse(RegistroVentaCreate):
    id_registro: int
    precio_unitario: float = Field(description="Precio inyectado por el sistema")
    subtotal: float = Field(description="Calculado automáticamente")
    class Config:
        from_attributes = True

class RegistroVentaPaginatedResponse(BaseModel):
    meta: PaginatedMeta
    rows: List[RegistroVentaResponse]
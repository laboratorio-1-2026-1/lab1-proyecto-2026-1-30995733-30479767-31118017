from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class VentaProductoBase(BaseModel):
    id_cliente: int
    id_metodo: int
    fecha_venta: datetime
    monto_total: float
    referencia: Optional[str] = None
    estado_venta: Optional[str] = "Completada"

class VentaProductoCreate(VentaProductoBase):
    pass

class VentaProductoResponse(VentaProductoBase):
    id_venta: int

    class Config:
        from_attributes = True
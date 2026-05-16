from pydantic import BaseModel

class RegistroVentaBase(BaseModel):
    id_venta: int
    id_producto: int
    cantidad: int
    precio_unitario: float
    subtotal: float

class RegistroVentaCreate(RegistroVentaBase):
    pass

class RegistroVentaResponse(RegistroVentaBase):
    id_registro: int

    class Config:
        from_attributes = True
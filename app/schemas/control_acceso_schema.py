from pydantic import BaseModel
from datetime import datetime

class ControlAccesoBase(BaseModel):
    id_cliente: int
    fecha_entrada: datetime

class ControlAccesoCreate(ControlAccesoBase):
    pass

class ControlAccesoResponse(ControlAccesoBase):
    id_acceso: int

    class Config:
        from_attributes = True
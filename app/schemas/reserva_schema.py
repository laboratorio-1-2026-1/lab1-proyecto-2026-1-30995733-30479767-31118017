from pydantic import BaseModel
from datetime import datetime

class ReservaBase(BaseModel):
    id_cliente: int
    id_sesion: int
    fecha_reserva: datetime

class ReservaCreate(ReservaBase):
    pass

class ReservaResponse(ReservaBase):
    id_reserva: int

    class Config:
        from_attributes = True
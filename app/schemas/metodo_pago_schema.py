from pydantic import BaseModel

class MetodoPagoBase(BaseModel):
    nombre_metodo: str


class MetodoPagoCreate(MetodoPagoBase):
    pass


class MetodoPagoResponse(MetodoPagoBase):
    id_metodo: int

    class Config:
        from_attributes = True
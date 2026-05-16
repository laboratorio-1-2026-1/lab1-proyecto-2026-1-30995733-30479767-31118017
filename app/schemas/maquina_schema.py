from pydantic import BaseModel
from typing import Optional

class MaquinaBase(BaseModel):
    id_categoria: int
    nombre: str
    estado_maquina: Optional[str] = "Operativa"

class MaquinaCreate(MaquinaBase):
    pass

class MaquinaResponse(MaquinaBase):
    id_maquina: int 

    class Config:
        from_attributes = True
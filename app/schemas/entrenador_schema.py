from pydantic import BaseModel
from typing import Optional

class EntrenadorBase(BaseModel):
    id_usuario: int
    nombre_ent: str
    apellido_ent: str
    especialidad: Optional[str] = None

class EntrenadorCreate(EntrenadorBase):
    pass

class EntrenadorResponse(EntrenadorBase):
    id_entrenador: int

    class Config:
        from_attributes = True
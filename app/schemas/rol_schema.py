from pydantic import BaseModel
from typing import Optional

class RolBase(BaseModel):
    nombre_rol: str
    descripcion: Optional[str] = None 

class RolCreate(RolBase):
    pass

class RolResponse(RolBase):
    id_rol: int

    class Config:
        from_attributes = True
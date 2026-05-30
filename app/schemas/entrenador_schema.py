from pydantic import BaseModel
from typing import Optional, List
from app.schemas.paginacion_schema import PaginatedMeta

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

class EntrenadorUpdate(BaseModel):
    nombre_ent: Optional[str] = None
    apellido_ent: Optional[str] = None
    especialidad: Optional[str] = None

class EntrenadorPaginatedResponse(BaseModel):
    meta: PaginatedMeta
    rows: List[EntrenadorResponse]
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from app.schemas.paginacion_schema import PaginatedMeta

class SesionClaseBase(BaseModel):
    id_disciplina: int
    id_entrenador: int
    fecha_inic: datetime
    fecha_fin: datetime
    cupos: int

class SesionClaseCreate(SesionClaseBase):
    pass

class SesionClaseResponse(SesionClaseBase):
    id_sesion: int  

    class Config:
        from_attributes = True

class SesionClaseUpdate(BaseModel):
    id_disciplina: Optional[int] = None
    id_entrenador: Optional[int] = None
    fecha_inic: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    cupos: Optional[int] = None

class SesionClasePaginatedResponse(BaseModel):
    meta: PaginatedMeta
    rows: List[SesionClaseResponse]
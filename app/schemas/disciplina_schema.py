from pydantic import BaseModel, Field
from typing import Optional, List
from app.schemas.paginacion_schema import PaginatedMeta

class DisciplinaBase(BaseModel):
    nombre_disc: str = Field(..., min_length=0, max_length=50, description="Nombre de la disciplina deportiva")
    descripcion: Optional[str] = Field(default=None, max_length=255, description="Descripción detallada de la disciplina")

class DisciplinaCreate(DisciplinaBase):
    pass

class DisciplinaResponse(DisciplinaBase):
    id_disciplina: int

    class Config:
        from_attributes = True


class DisciplinaUpdate(BaseModel):
    nombre_disc: Optional[str] = Field(default=None, min_length=0, max_length=50)
    descripcion: Optional[str] = Field(default=None, max_length=255)

class DisciplinaPaginatedResponse(BaseModel):
    meta: PaginatedMeta
    rows: List[DisciplinaResponse]
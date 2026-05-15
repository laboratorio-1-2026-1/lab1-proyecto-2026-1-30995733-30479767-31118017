from pydantic import BaseModel
from typing import Optional

class DisciplinaBase(BaseModel):
    nombre_disc: str
    descripcion: Optional[str] = None


class DisciplinaCreate(DisciplinaBase):
    pass

class DisciplinaResponse(DisciplinaBase):
    id_disciplina: int

    class Config:
        from_attributes = True
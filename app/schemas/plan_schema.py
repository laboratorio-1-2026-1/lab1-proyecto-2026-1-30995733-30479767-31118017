from pydantic import BaseModel
from typing import Optional

class PlanBase(BaseModel):
    nombre_plan: str
    precio_sub: float      # Cambiado para que coincida con el Model
    duracion_dias: int     # Cambiado para que coincida con el Model
    descripcion: Optional[str] = None

class PlanCreate(PlanBase):
    pass

class PlanResponse(PlanBase):
    id_plan: int

    class Config:
        from_attributes = True
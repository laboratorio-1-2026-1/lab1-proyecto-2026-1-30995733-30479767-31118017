from pydantic import BaseModel
from typing import Optional, List
from app.schemas.paginacion_schema import PaginatedMeta

class PlanBase(BaseModel):
    nombre_plan: str
    precio_sub: float
    duracion_dias: int
    descripcion: Optional[str] = None

class PlanCreate(PlanBase):
    pass

class PlanResponse(PlanBase):
    id_plan: int

    class Config:
        from_attributes = True

class PlanUpdate(BaseModel):
    nombre_plan: Optional[str] = None
    precio_sub: Optional[float] = None
    duracion_dias: Optional[int] = None
    descripcion: Optional[str] = None

class PlanPaginatedResponse(BaseModel):
    meta: PaginatedMeta
    rows: List[PlanResponse]
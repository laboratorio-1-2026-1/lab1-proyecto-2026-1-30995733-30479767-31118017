from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from app.schemas.paginacion_schema import PaginatedMeta

class MaquinaBase(BaseModel):
    id_categoria: int = Field(..., gt=0, description="ID de la categoría a la que pertenece la máquina")
    nombre: str = Field(..., min_length=0, max_length=100, description="Nombre descriptivo de la máquina")
    descripcion_tecnica: Optional[str] = Field(default=None, max_length=255, description="Especificaciones técnicas")
    estado_maquina: Optional[str] = Field(default="Operativa", description="Estado operativo actual")

    @field_validator('estado_maquina')
    @classmethod
    def validar_estado(cls, v):
        estados_permitidos = ["Operativa", "En Mantenimiento", "Fuera de Servicio"]
        if v and v not in estados_permitidos:
            raise ValueError(f"Estado inválido. Usa solo: {', '.join(estados_permitidos)}")
        return v

class MaquinaCreate(MaquinaBase):
    pass

class MaquinaResponse(MaquinaBase):
    id_maquina: int 

    class Config:
        from_attributes = True

class MaquinaUpdate(BaseModel):
    id_categoria: Optional[int] = Field(default=None, gt=0)
    nombre: Optional[str] = Field(default=None, min_length=0, max_length=100)
    descripcion_tecnica: Optional[str] = Field(default=None, max_length=255)
    estado_maquina: Optional[str] = None

    @field_validator('estado_maquina')
    @classmethod
    def validar_estado_update(cls, v):
        estados_permitidos = ["Operativa", "En Mantenimiento", "Fuera de Servicio"]
        if v and v not in estados_permitidos:
            raise ValueError(f"Estado inválido. Usa solo: {', '.join(estados_permitidos)}")
        return v

class MaquinaPaginatedResponse(BaseModel):
    meta: PaginatedMeta
    rows: List[MaquinaResponse]
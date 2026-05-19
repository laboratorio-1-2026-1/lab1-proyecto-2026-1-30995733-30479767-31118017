from pydantic import BaseModel, Field, field_validator
from typing import Optional

class MaquinaBase(BaseModel):
    id_categoria: int = Field(..., gt=0, description="ID de la categoría a la que pertenece la máquina")
    nombre: str = Field(..., min_length=3, max_length=100, description="Nombre descriptivo de la máquina")
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
    id_categoria: Optional[int] = None
    nombre: Optional[str] = None
    estado_maquina: Optional[str] = None
from pydantic import BaseModel, EmailStr
from typing import List
from app.schemas.paginacion_schema import PaginatedMeta

class UsuarioBase(BaseModel):
    email: EmailStr 
    id_rol: int

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioResponse(UsuarioBase):
    id_user: int
    
    class Config:
        from_attributes = True

class UsuarioPaginatedResponse(BaseModel):
    meta: PaginatedMeta
    rows: List[UsuarioResponse]
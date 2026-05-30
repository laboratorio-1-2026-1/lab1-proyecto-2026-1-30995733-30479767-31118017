from pydantic import BaseModel, EmailStr
from typing import List, Optional
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


class UsuarioUpdate(BaseModel):
    email: Optional[EmailStr] = None
    id_rol: Optional[int] = None
    estatus_usuario: Optional[bool] = None

class UsuarioPaginatedResponse(BaseModel):
    meta: PaginatedMeta
    rows: List[UsuarioResponse]
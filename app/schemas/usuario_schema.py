from pydantic import BaseModel, EmailStr

class UsuarioBase(BaseModel):
    email: EmailStr 
    id_rol: int

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioResponse(UsuarioBase):
    id_user: int
    
    class Config:
        from_attributes = True
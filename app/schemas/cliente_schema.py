from pydantic import BaseModel

class ClienteBase(BaseModel):
    id_usuario: int
    nombre_cli: str
    apellido_cli: str
    cedula: str

class ClienteCreate(ClienteBase):
    pass

class ClienteResponse(ClienteBase):
    id_cliente: int

    class Config:
        from_attributes = True
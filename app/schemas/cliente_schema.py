from pydantic import BaseModel
from typing import List
from app.schemas.paginacion_schema import PaginatedMeta
from typing import Optional

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

class ClientePaginatedResponse(BaseModel):
    meta: PaginatedMeta
    rows: List[ClienteResponse]

class ClienteUpdate(BaseModel):
    nombre_cli: Optional[str] = None
    apellido_cli: Optional[str] = None
    cedula: Optional[str] = None
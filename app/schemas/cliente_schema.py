from pydantic import BaseModel
from typing import List
from app.schemas.paginacion_schema import PaginatedMeta

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
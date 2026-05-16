from pydantic import BaseModel

class ProductoBase(BaseModel):
    nombre_prod: str
    precio: float
    stock: int

class ProductoCreate(ProductoBase):
    pass

class ProductoResponse(ProductoBase):
    id_producto: int 

    class Config:
        from_attributes = True
from pydantic import BaseModel

class CategoriaMaquinaBase(BaseModel):
    nombre_categoria: str

class CategoriaMaquinaCreate(CategoriaMaquinaBase):
    pass

class CategoriaMaquinaResponse(CategoriaMaquinaBase):
    id_categoria: int

    class Config:
        from_attributes = True
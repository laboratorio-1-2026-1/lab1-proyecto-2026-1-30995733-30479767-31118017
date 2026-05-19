from app.crud.base import CRUDBase
from app.models.categoria_maquina import CategoriaMaquina

class CRUDCategoria(CRUDBase[CategoriaMaquina]): 
    pass

categoria = CRUDCategoria(CategoriaMaquina)
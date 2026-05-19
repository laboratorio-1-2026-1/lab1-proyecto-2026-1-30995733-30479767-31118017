from app.crud.base import CRUDBase
from app.models.producto import Producto

class CRUDProducto(CRUDBase[Producto]):
    pass

producto = CRUDProducto(Producto)
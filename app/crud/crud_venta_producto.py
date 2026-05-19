from app.crud.base import CRUDBase
from app.models.venta_producto import VentaProducto
class CRUDVentaProducto(CRUDBase[VentaProducto]):
    pass

venta_producto = CRUDVentaProducto(VentaProducto)
from app.crud.base import CRUDBase
from app.models.registro_venta import RegistroVenta

class CRUDRegistroVenta(CRUDBase[RegistroVenta]):
    pass

registro_venta = CRUDRegistroVenta(RegistroVenta)
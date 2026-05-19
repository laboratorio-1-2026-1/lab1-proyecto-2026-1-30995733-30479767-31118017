from app.crud.base import CRUDBase
from app.models.rol import Rol

class CRUDRol(CRUDBase[Rol]):
    pass

rol = CRUDRol(Rol)
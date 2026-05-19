from app.crud.base import CRUDBase
from app.models.membresia import Membresia 

class CRUDMembresia(CRUDBase[Membresia]):
    pass

membresia = CRUDMembresia(Membresia)
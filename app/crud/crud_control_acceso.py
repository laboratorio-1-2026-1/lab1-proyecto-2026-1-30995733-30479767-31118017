from app.crud.base import CRUDBase
from app.models.control_acceso import ControlAcceso

class CRUDControlAcceso(CRUDBase[ControlAcceso]):
    pass

control_acceso = CRUDControlAcceso(ControlAcceso)
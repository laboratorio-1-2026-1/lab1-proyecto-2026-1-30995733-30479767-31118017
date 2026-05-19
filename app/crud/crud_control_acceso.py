from app.crud.base import CRUDBase
from app.models.control_acceso import ControlAcceso 

class CRUDControlAcceso(CRUDBase[ControlAcceso]):
    """
    Operaciones CRUD para el Control de Acceso (Entradas/Asistencias).
    """
    pass

control_acceso = CRUDControlAcceso(ControlAcceso)
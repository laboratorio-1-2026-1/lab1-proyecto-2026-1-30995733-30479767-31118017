from app.crud.base import CRUDBase
from app.models.sesion_clase import SesionClase

class CRUDSesion(CRUDBase[SesionClase]):
    pass

sesion = CRUDSesion(SesionClase)
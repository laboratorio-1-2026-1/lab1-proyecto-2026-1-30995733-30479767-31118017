from app.crud.base import CRUDBase
from app.models.maquina import Maquina 

class CRUDMaquina(CRUDBase[Maquina]):
    pass

maquina = CRUDMaquina(Maquina)
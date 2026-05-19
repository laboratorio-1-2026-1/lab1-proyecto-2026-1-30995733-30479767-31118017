from app.crud.base import CRUDBase
from app.models.entrenador import Entrenador

class CRUDEntrenador(CRUDBase[Entrenador]):
    pass

entrenador = CRUDEntrenador(Entrenador)
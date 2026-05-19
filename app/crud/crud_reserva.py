from app.crud.base import CRUDBase
from app.models.reserva import Reserva

class CRUDReserva(CRUDBase[Reserva]):
    pass

reserva = CRUDReserva(Reserva)
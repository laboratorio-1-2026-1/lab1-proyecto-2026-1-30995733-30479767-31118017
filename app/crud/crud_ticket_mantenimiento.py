from app.crud.base import CRUDBase
from app.models.ticket_mantenimiento import TicketMantenimiento 

class CRUDTicketMantenimiento(CRUDBase[TicketMantenimiento]):
    pass

ticket_mantenimiento = CRUDTicketMantenimiento(TicketMantenimiento)
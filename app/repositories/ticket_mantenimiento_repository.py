from sqlalchemy.orm import Session
from typing import Optional
from app.repositories.base import CRUDBase
from app.models.ticket_mantenimiento_model import TicketMantenimiento

class CRUDTicketMantenimiento(CRUDBase[TicketMantenimiento]):
    
    def obtener_query_filtrada(self, db: Session, id_maquina: Optional[int] = None):

        query = db.query(self.model)
        
        if id_maquina is not None:
            query = query.filter(self.model.id_maquina == id_maquina)
            
        return query.order_by(self.model.fecha_falla.desc())

ticket_mantenimiento = CRUDTicketMantenimiento(TicketMantenimiento)
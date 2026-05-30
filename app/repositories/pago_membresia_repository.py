from sqlalchemy.orm import Session
from typing import Optional
from app.repositories.base import CRUDBase
from app.models.pago_membresia_model import PagoMembresia

class CRUDPagoMembresia(CRUDBase[PagoMembresia]):
    
    def get_by_referencia(self, db: Session, referencia: str) -> Optional[PagoMembresia]:
        return db.query(self.model).filter(self.model.referencia == referencia).first()

    def obtener_query_filtrada(self, db: Session, id_cliente: Optional[int] = None):
        query = db.query(self.model)
        
        if id_cliente is not None:
            query = query.filter(self.model.id_cliente == id_cliente)
            
        return query.order_by(self.model.fecha_pago.desc())

pago_membresia = CRUDPagoMembresia(PagoMembresia)
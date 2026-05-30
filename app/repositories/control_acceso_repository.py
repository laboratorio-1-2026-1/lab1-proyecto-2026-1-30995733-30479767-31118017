from sqlalchemy.orm import Session
from typing import Optional
from app.repositories.base import CRUDBase
from app.models.control_acceso_model import ControlAcceso
from app.models.cliente_model import Cliente

class CRUDControlAcceso(CRUDBase[ControlAcceso]):
    
    def obtener_query_filtrada(self, db: Session, cedula: Optional[str] = None):

        query = db.query(self.model)
        
        if cedula:
            query = query.join(Cliente, self.model.id_cliente == Cliente.id_cliente)\
                         .filter(Cliente.cedula.ilike(f"%{cedula}%"))
            
        return query.order_by(self.model.fecha_entrada.desc())

control_acceso = CRUDControlAcceso(ControlAcceso)
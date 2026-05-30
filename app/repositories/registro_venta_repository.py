from sqlalchemy.orm import Session
from typing import Optional
from app.repositories.base import CRUDBase
from app.models.registro_venta_model import RegistroVenta

class CRUDRegistroVenta(CRUDBase[RegistroVenta]):
    
    def obtener_query_filtrada(self, db: Session, id_producto: Optional[int] = None, id_venta: Optional[int] = None):

        query = db.query(self.model)
        
        if id_producto:
            query = query.filter(self.model.id_producto == id_producto)
            
        if id_venta:
            query = query.filter(self.model.id_venta == id_venta)
            
        return query

registro_venta = CRUDRegistroVenta(RegistroVenta)
from sqlalchemy.orm import Session
from typing import Optional
from app.repositories.base import CRUDBase
from app.models.venta_producto_model import VentaProducto

class CRUDVentaProducto(CRUDBase[VentaProducto]):
    
    def obtener_query_filtrada(self, db: Session, id_cliente: Optional[int] = None):

        query = db.query(self.model)
        
        if id_cliente:
            query = query.filter(self.model.id_cliente == id_cliente)
            
        query = query.order_by(self.model.fecha_venta.desc())
        
        return query

venta_producto = CRUDVentaProducto(VentaProducto)
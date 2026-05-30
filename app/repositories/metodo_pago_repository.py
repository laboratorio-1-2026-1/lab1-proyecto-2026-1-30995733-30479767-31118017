from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from app.repositories.base import CRUDBase
from app.models.metodo_pago_model import MetodoPago

class CRUDMetodoPago(CRUDBase[MetodoPago]):
    
    def get_by_nombre(self, db: Session, nombre_metodo: str) -> Optional[MetodoPago]:

        return db.query(self.model).filter(
            func.lower(self.model.nombre_metodo) == func.lower(nombre_metodo)
        ).first()

    def obtener_query_filtrada(self, db: Session, nombre_metodo: Optional[str] = None):

        query = db.query(self.model)
        if nombre_metodo:
            query = query.filter(self.model.nombre_metodo.ilike(f"%{nombre_metodo}%"))
        return query

metodo_pago = CRUDMetodoPago(MetodoPago)
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from app.repositories.base import CRUDBase
from app.models.producto_model import Producto

class CRUDProducto(CRUDBase[Producto]):
    
    def get_by_nombre(self, db: Session, nombre_prod: str) -> Optional[Producto]:

        return db.query(self.model).filter(
            func.lower(self.model.nombre_prod) == func.lower(nombre_prod)
        ).first()

    def obtener_query_filtrada(self, db: Session, nombre_filtro: Optional[str] = None):

        query = db.query(self.model)
        if nombre_filtro:
            query = query.filter(self.model.nombre_prod.ilike(f"%{nombre_filtro}%"))
        return query

producto = CRUDProducto(Producto)
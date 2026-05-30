from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from app.repositories.base import CRUDBase
from app.models.rol_model import Rol

class CRUDRol(CRUDBase[Rol]):
    
    def get_by_nombre(self, db: Session, nombre_rol: str) -> Optional[Rol]:
        return db.query(self.model).filter(func.lower(self.model.nombre_rol) == func.lower(nombre_rol)).first()

    def obtener_query_filtrada(self, db: Session, nombre_filtro: Optional[str] = None):
        query = db.query(self.model)
        if nombre_filtro:
            query = query.filter(self.model.nombre_rol.ilike(f"%{nombre_filtro}%"))
        return query

rol = CRUDRol(Rol)
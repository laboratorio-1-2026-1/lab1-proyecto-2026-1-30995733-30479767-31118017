from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from app.repositories.base import CRUDBase
from app.models.categoria_maquina_model import CategoriaMaquina

class CRUDCategoria(CRUDBase[CategoriaMaquina]): 
    
    def get_by_nombre(self, db: Session, nombre_categoria: str) -> Optional[CategoriaMaquina]:

        return db.query(self.model).filter(
            func.lower(self.model.nombre_categoria) == func.lower(nombre_categoria)
        ).first()

    def obtener_query_filtrada(self, db: Session, nombre_filtro: Optional[str] = None):

        query = db.query(self.model)
        if nombre_filtro:
            query = query.filter(self.model.nombre_categoria.ilike(f"%{nombre_filtro}%"))
        return query

categoria = CRUDCategoria(CategoriaMaquina)
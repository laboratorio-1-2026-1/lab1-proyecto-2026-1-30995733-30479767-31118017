from sqlalchemy.orm import Session
from typing import Optional
from app.repositories.base import CRUDBase
from app.models.maquina_model import Maquina

class CRUDMaquina(CRUDBase[Maquina]):
    
    def obtener_query_filtrada(self, db: Session, estado: Optional[str] = None, id_cat: Optional[int] = None):

        query = db.query(self.model)
        
        if id_cat is not None:
            query = query.filter(self.model.id_categoria == id_cat)
            
        if estado is not None and estado.strip():
            query = query.filter(self.model.estado_maquina.ilike(f"%{estado.strip()}%"))
            
        return query

maquina = CRUDMaquina(Maquina)
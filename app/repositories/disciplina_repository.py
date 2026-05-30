from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from app.repositories.base import CRUDBase
from app.models.disciplina_model import Disciplina

class CRUDDisciplina(CRUDBase[Disciplina]):
    
    def get_by_nombre(self, db: Session, nombre_disc: str) -> Optional[Disciplina]:

        return db.query(self.model).filter(
            func.lower(self.model.nombre_disc) == func.lower(nombre_disc)
        ).first()

    def obtener_query_filtrada(self, db: Session, nombre_filtro: Optional[str] = None):

        query = db.query(self.model)
        if nombre_filtro:
            query = query.filter(self.model.nombre_disc.ilike(f"%{nombre_filtro}%"))
        return query

disciplina = CRUDDisciplina(Disciplina)
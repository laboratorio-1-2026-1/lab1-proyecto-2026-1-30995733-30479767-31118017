from sqlalchemy.orm import Session
from typing import Optional
from app.repositories.base import CRUDBase
from app.models.entrenador_model import Entrenador

class CRUDEntrenador(CRUDBase[Entrenador]):
    
    def get_by_usuario_id(self, db: Session, id_usuario: int) -> Optional[Entrenador]:

        return db.query(self.model).filter(self.model.id_usuario == id_usuario).first()

    def obtener_query_filtrada(self, db: Session, especialidad: Optional[str] = None):

        query = db.query(self.model)
        if especialidad:
            query = query.filter(self.model.especialidad.ilike(f"%{especialidad}%"))
        return query

entrenador = CRUDEntrenador(Entrenador)
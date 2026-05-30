from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from app.repositories.base import CRUDBase
from app.models.sesion_clase_model import SesionClase

class CRUDSesion(CRUDBase[SesionClase]):
    
    def verificar_choque_entrenador(
        self, db: Session, id_entrenador: int, inicio: datetime, fin: datetime, id_sesion_excluir: Optional[int] = None
    ) -> Optional[SesionClase]:

        query = db.query(self.model).filter(
            self.model.id_entrenador == id_entrenador,
            inicio < self.model.fecha_fin,
            fin > self.model.fecha_inic
        )

        if id_sesion_excluir:
            query = query.filter(self.model.id_sesion != id_sesion_excluir)
            
        return query.first()

    def obtener_query_filtrada(
        self, db: Session, id_disciplina: Optional[int] = None, id_entrenador: Optional[int] = None
    ):

        query = db.query(self.model)
        
        if id_disciplina:
            query = query.filter(self.model.id_disciplina == id_disciplina)
        if id_entrenador:
            query = query.filter(self.model.id_entrenador == id_entrenador)
            
        return query.order_by(self.model.fecha_inic.asc())

sesion = CRUDSesion(SesionClase)
from sqlalchemy.orm import Session
from typing import Optional
from app.repositories.base import CRUDBase
from app.models.evaluacion_biometrica_model import EvaluacionBiometrica

class CRUDEvaluacionBiometrica(CRUDBase[EvaluacionBiometrica]):
    
    def obtener_query_filtrada(
        self, db: Session, id_cliente: Optional[int] = None, orden_fecha: str = "desc"
    ):

        query = db.query(self.model)
        
        if id_cliente is not None:
            query = query.filter(self.model.id_cliente == id_cliente)
            
        if orden_fecha.strip().lower() == "asc":
            query = query.order_by(self.model.fecha.asc())
        else:
            query = query.order_by(self.model.fecha.desc())
            
        return query

evaluacion = CRUDEvaluacionBiometrica(EvaluacionBiometrica)
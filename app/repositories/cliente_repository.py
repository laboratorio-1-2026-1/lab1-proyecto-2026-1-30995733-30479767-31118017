from sqlalchemy.orm import Session
from typing import Optional
from app.repositories.base import CRUDBase
from app.models.cliente_model import Cliente

class CRUDCliente(CRUDBase[Cliente]):
    
    def get_by_cedula(self, db: Session, cedula: str) -> Optional[Cliente]:
        return db.query(self.model).filter(self.model.cedula == cedula).first()

    def get_by_usuario_id(self, db: Session, id_usuario: int) -> Optional[Cliente]:
        return db.query(self.model).filter(self.model.id_usuario == id_usuario).first()

    def obtener_query_filtrada(self, db: Session, cedula: Optional[str] = None):
        query = db.query(self.model)
        if cedula:
            query = query.filter(self.model.cedula.ilike(f"%{cedula}%"))
        return query

cliente = CRUDCliente(Cliente)
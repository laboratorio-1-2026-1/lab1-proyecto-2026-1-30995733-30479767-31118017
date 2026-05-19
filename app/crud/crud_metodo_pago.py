from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.metodo_pago import MetodoPago

class CRUDMetodoPago(CRUDBase[MetodoPago]):
    
    def get_by_nombre(self, db: Session, nombre_metodo: str) -> MetodoPago:
        """
        Busca un método de pago por su nombre exacto en PostgreSQL.
        """
        return db.query(self.model).filter(self.model.nombre_metodo == nombre_metodo).first()

metodo_pago = CRUDMetodoPago(MetodoPago)
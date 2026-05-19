from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.pago_membresia import PagoMembresia

class CRUDPagoMembresia(CRUDBase[PagoMembresia]):
    def get_by_referencia(self, db: Session, referencia: str) -> PagoMembresia:
        """
        Obtiene de manera directa un registro de pago filtrando por su referencia.
        """
        return db.query(self.model).filter(self.model.referencia == referencia).first()

pago_membresia = CRUDPagoMembresia(PagoMembresia)
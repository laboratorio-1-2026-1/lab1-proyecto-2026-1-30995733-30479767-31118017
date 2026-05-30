from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from app.repositories.base import CRUDBase
from app.models.reserva_model import Reserva
from app.models.sesion_clase_model import SesionClase

class CRUDReserva(CRUDBase[Reserva]):
    
    def contar_por_sesion(self, db: Session, id_sesion: int) -> int:
        return db.query(self.model).filter(self.model.id_sesion == id_sesion).count()

    def verificar_solapamiento(
        self, db: Session, id_cliente: int, fecha_inic: datetime, fecha_fin: datetime, id_reserva_excluida: Optional[int] = None
    ) -> Optional[Reserva]:
        query = db.query(self.model).join(SesionClase, self.model.id_sesion == SesionClase.id_sesion).filter(
            self.model.id_cliente == id_cliente,
            fecha_inic < SesionClase.fecha_fin,
            fecha_fin > SesionClase.fecha_inic
        )
        if id_reserva_excluida:
            query = query.filter(self.model.id_reserva != id_reserva_excluida)
            
        return query.first()

    def obtener_query_filtrada(self, db: Session, id_cliente: Optional[int] = None, id_sesion: Optional[int] = None):

        query = db.query(self.model)
        if id_cliente:
            query = query.filter(self.model.id_cliente == id_cliente)
        if id_sesion:
            query = query.filter(self.model.id_sesion == id_sesion)
        return query

reserva = CRUDReserva(Reserva)
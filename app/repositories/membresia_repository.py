from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import date
from typing import Optional
from app.repositories.base import CRUDBase
from app.models.membresia_model import Membresia

class CRUDMembresia(CRUDBase[Membresia]):
    
    def get_by_pago_id(self, db: Session, id_pago: int) -> Optional[Membresia]:
        return db.query(self.model).filter(self.model.id_pago == id_pago).first()

    def verificar_membresia_activa(self, db: Session, id_cliente: int, fecha_referencia: date) -> bool:
        membresia_valida = db.query(self.model).filter(
            self.model.id_cliente == id_cliente,
            self.model.estado == True,
            self.model.fecha_fin >= fecha_referencia
        ).first()
        return membresia_valida is not None

    def verificar_superposicion_fechas(
        self, db: Session, id_cliente: int, fecha_inicio: date, fecha_fin: date, id_membresia_excluir: Optional[int] = None
    ) -> Optional[Membresia]:
        query = db.query(self.model).filter(
            self.model.id_cliente == id_cliente,
            self.model.estado == True,
            fecha_inicio <= self.model.fecha_fin,
            fecha_fin >= self.model.fecha_inicio
        )
        if id_membresia_excluir:
            query = query.filter(self.model.id_membresia != id_membresia_excluir)
        return query.first()

    def obtener_query_filtrada(self, db: Session, id_cliente: Optional[int] = None, estado: Optional[bool] = None):
        query = db.query(self.model)
        if id_cliente is not None:
            query = query.filter(self.model.id_cliente == id_cliente)
        if estado is not None:
            query = query.filter(self.model.estado == estado)
        return query.order_by(self.model.fecha_inicio.desc())
membresia = CRUDMembresia(Membresia)
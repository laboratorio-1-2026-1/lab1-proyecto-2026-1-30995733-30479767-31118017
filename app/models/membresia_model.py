from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime, date, timedelta

class Membresia(Base):
    __tablename__ = "membresia"

    id_membresia = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("cliente.id_cliente"), nullable=False)
    id_plan = Column(Integer, ForeignKey("plan_subscripcion.id_plan"), nullable=False)
    id_pago = Column(Integer, ForeignKey("pago_membresia.id_pago"), nullable=False)
    fecha_inicio = Column(DateTime, nullable=False)
    fecha_fin = Column(DateTime, nullable=False)
    estado = Column(Boolean, default=True)

    @property
    def estado_dinamico(self) -> str:
        hoy = date.today()
        f_fin = self.fecha_fin.date() if isinstance(self.fecha_fin, datetime) else self.fecha_fin
        
        if hoy > f_fin:
            return "Vencida"
        if f_fin - timedelta(days=5) <= hoy <= f_fin:
            return "Por Vencer"
        return "Activa"

    cliente = relationship("Cliente", back_populates="membresias")
    plan = relationship("PlanSubscripcion", back_populates="membresias")
    pago = relationship("PagoMembresia", back_populates="membresias")
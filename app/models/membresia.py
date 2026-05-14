from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Membresia(Base):
    __tablename__ = "membresia"

    id_membresia = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("cliente.id_cliente"), nullable=False)
    id_plan = Column(Integer, ForeignKey("plan_subscripcion.id_plan"), nullable=False)
    id_pago = Column(Integer, ForeignKey("pago_membresia.id_pago"), nullable=False)
    fecha_inicio = Column(DateTime, nullable=False)
    fecha_fin = Column(DateTime, nullable=False)
    estado = Column(Boolean, default=True)

    #En el MER vemos que se relaciona con:
    cliente = relationship("Cliente", back_populates="membresias")
    plan = relationship("PlanSubscripcion", back_populates="membresias")
    pago = relationship("PagoMembresia", back_populates="membresias")
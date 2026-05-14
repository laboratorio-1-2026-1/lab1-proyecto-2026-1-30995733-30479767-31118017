from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime

class PagoMembresia(Base):
    __tablename__ = "pago_membresia"

    id_pago = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("cliente.id_cliente"), nullable=False)
    id_metodo = Column(Integer, ForeignKey("metodo_pago.id_metodo"), nullable=False)
    monto_membresia = Column(Float, nullable=False)
    referencia = Column(String(100), nullable=True, unique=True)
    fecha_pago = Column(DateTime, default=datetime.utcnow)
    estado_pago = Column(String(50), nullable=False, default="Completado")

    #En el MER vemos que se relaciona con:
    cliente = relationship("Cliente", back_populates="pagos")
    metodo = relationship("MetodoPago", back_populates="pagos_membresia")
    membresias = relationship("Membresia", back_populates="pago")
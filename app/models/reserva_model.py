from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime

class Reserva(Base):
    __tablename__ = "reserva"

    id_reserva = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("cliente.id_cliente"), nullable=False)
    id_sesion = Column(Integer, ForeignKey("sesion_clase.id_sesion"), nullable=False)
    fecha_reserva = Column(DateTime, default=datetime.utcnow)

    cliente = relationship("Cliente", back_populates="reservas")
    sesion = relationship("SesionClase", back_populates="reservas")
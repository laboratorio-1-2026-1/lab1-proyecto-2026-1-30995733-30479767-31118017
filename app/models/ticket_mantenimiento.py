from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime

class TicketMantenimiento(Base):
    __tablename__ = "ticket_mantenimiento"

    id_ticket = Column(Integer, primary_key=True, index=True)
    id_maquina = Column(Integer, ForeignKey("maquina.id_maquina"), nullable=False)
    desc_fallo = Column(Text, nullable=False)
    costo_reparacion = Column(Float, nullable=True)  # Puede ser nulo mientras el ticket esté abierto
    fecha_falla = Column(DateTime, default=datetime.utcnow)
    fecha_resolucion = Column(DateTime, nullable=True)  # Nula si está pendiente

    #En el MER vemos que se relaciona con:
    maquina = relationship("Maquina", back_populates="tickets")
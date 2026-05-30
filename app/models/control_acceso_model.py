from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime

class ControlAcceso(Base):
    __tablename__ = "control_acceso"

    id_acceso = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("cliente.id_cliente"), nullable=False)
    fecha_entrada = Column(DateTime, default=datetime.utcnow)
    
    cliente = relationship("Cliente", back_populates="asistencias")
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Maquina(Base):
    __tablename__ = "maquina"

    id_maquina = Column(Integer, primary_key=True, index=True)
    id_categoria = Column(Integer, ForeignKey("categoria_maquina.id_categoria"), nullable=False)
    nombre = Column(String(100), nullable=False)
    descripcion_tecnica = Column(String(255), nullable=True)
    estado_maquina = Column(String(50), default="Operativa")

    categoria = relationship("CategoriaMaquina", back_populates="maquinas")
    tickets = relationship("TicketMantenimiento", back_populates="maquina")
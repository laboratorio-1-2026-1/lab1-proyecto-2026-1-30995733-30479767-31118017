from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class SesionClase(Base):
    __tablename__ = "sesion_clase"

    id_sesion = Column(Integer, primary_key=True, index=True)
    id_disciplina = Column(Integer, ForeignKey("disciplina.id_disciplina"), nullable=False)
    id_entrenador = Column(Integer, ForeignKey("entrenador.id_entrenador"), nullable=False)
    fecha_inic = Column(DateTime, nullable=False)
    fecha_fin = Column(DateTime, nullable=False)
    cupos = Column(Integer, nullable=False)

    @property
    def cupos_disponibles(self) -> int:
        reservas_ocupadas = len(self.reservas) 
        return max(0, self.cupos - reservas_ocupadas)
    
    disciplina = relationship("Disciplina", back_populates="sesiones")
    reservas = relationship("Reserva", back_populates="sesion")
    entrenador = relationship("Entrenador", back_populates="sesiones")
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime

class EvaluacionBiometrica(Base):
    __tablename__ = "evaluacion_biometrica"

    id_evaluacion = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("cliente.id_cliente"), nullable=False)
    id_entrenador = Column(Integer, ForeignKey("entrenador.id_entrenador"), nullable=False)
    peso = Column(Float, nullable=False)
    altura = Column(Float, nullable=False)
    porc_grasa = Column(Float, nullable=False)
    observaciones = Column(Text)
    historial = Column(Text)
    fecha = Column(DateTime, default=datetime.utcnow)

    #En el MER vemos que se relaciona con:
    cliente = relationship("Cliente", back_populates="evaluaciones")
    entrenador = relationship("Entrenador", back_populates="evaluaciones")
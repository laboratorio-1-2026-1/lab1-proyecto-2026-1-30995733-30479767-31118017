from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Entrenador(Base):
    __tablename__ = "entrenador"

    id_entrenador = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuario.id_user"), nullable=False)
    nombre_ent = Column(String(100), nullable=False)
    apellido_ent = Column(String(100), nullable=False)
    especialidad = Column(String(100))

    #En el MER vemos que se relaciona con:
    usuario = relationship("Usuario", back_populates="entrenador")
    sesiones = relationship("SesionClase", back_populates="entrenador")
    evaluaciones = relationship("EvaluacionBiometrica", back_populates="entrenador")
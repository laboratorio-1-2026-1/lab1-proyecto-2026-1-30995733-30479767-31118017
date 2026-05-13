from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base

class Disciplina(Base):
    __tablename__ = "disciplina"

    id_disciplina = Column(Integer, primary_key=True, index=True)
    nombre_disc = Column(String(100), nullable=False)
    descripcion = Column(String(255))

    #En el MER vemos que se relaciona con:
    sesiones = relationship("SesionClase", back_populates="disciplina")
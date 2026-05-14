from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base

class Rol(Base):
    __tablename__ = "rol"

    id_rol = Column(Integer, primary_key=True, index=True)
    nombre_rol = Column(String(50), nullable=False, unique=True)
    descripcion = Column(String(200))

    #En el MER vemos que se relaciona con:
    usuarios = relationship("Usuario", back_populates="rol")
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base

class CategoriaMaquina(Base):
    __tablename__ = "categoria_maquina"

    id_categoria = Column(Integer, primary_key=True, index=True)
    nombre_categoria = Column(String(100), nullable=False, unique=True)

    maquinas = relationship("Maquina", back_populates="categoria")
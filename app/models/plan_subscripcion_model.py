from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.db.database import Base

class PlanSubscripcion(Base):
    __tablename__ = "plan_subscripcion"

    id_plan = Column(Integer, primary_key=True, index=True)
    nombre_plan = Column(String(100), nullable=False, unique=True)
    precio_sub = Column(Float, nullable=False)
    descripcion = Column(String(255))
    duracion_dias = Column(Integer, nullable=False)

    membresias = relationship("Membresia", back_populates="plan")
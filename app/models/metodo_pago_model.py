from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base

class MetodoPago(Base):
    __tablename__ = "metodo_pago"

    id_metodo = Column(Integer, primary_key=True, index=True)
    nombre_metodo = Column(String(50), nullable=False, unique=True)

    pagos_membresia = relationship("PagoMembresia", back_populates="metodo")
    ventas = relationship("VentaProducto", back_populates="metodo")
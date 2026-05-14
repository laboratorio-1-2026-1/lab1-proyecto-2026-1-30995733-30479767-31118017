from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class RegistroVenta(Base):
    __tablename__ = "registro_venta"

    id_registro = Column(Integer, primary_key=True, index=True)
    id_venta = Column(Integer, ForeignKey("venta_producto.id_venta"), nullable=False)
    id_producto = Column(Integer, ForeignKey("producto.id_producto"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False) 
    subtotal = Column(Float, nullable=False)

    #En el MER vemos que se relaciona con:
    venta = relationship("VentaProducto", back_populates="detalles")
    producto = relationship("Producto", back_populates="registros_venta")
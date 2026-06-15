from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime

class VentaProducto(Base):
    __tablename__ = "venta_producto"

    id_venta = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("cliente.id_cliente"), nullable=False)
    id_metodo = Column(Integer, ForeignKey("metodo_pago.id_metodo"), nullable=False)
    fecha_venta = Column(DateTime, default=datetime.now)
    monto_total = Column(Float, nullable=False)
    referencia = Column(String(100), nullable=True)
    estado_venta = Column(String(50), nullable=False, default="Pendiente")

    cliente = relationship("Cliente", back_populates="compras")
    metodo = relationship("MetodoPago", back_populates="ventas")
    detalles = relationship("RegistroVenta", back_populates="venta")
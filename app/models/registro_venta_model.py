from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from sqlalchemy import event

class RegistroVenta(Base):
    __tablename__ = "registro_venta"

    id_registro = Column(Integer, primary_key=True, index=True)
    id_venta = Column(Integer, ForeignKey("venta_producto.id_venta"), nullable=False)
    id_producto = Column(Integer, ForeignKey("producto.id_producto"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False) 
    subtotal = Column(Float, nullable=False)

    venta = relationship("VentaProducto", back_populates="detalles")
    producto = relationship("Producto", back_populates="registros_venta")

@event.listens_for(RegistroVenta, 'after_insert')
def actualizar_total_factura(mapper, connection, target):

    tabla_venta = target.metadata.tables['venta_producto']
    connection.execute(
        tabla_venta.update().
        where(tabla_venta.c.id_venta == target.id_venta).
        values(monto_total=tabla_venta.c.monto_total + target.subtotal)
    )
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Cliente(Base):
    __tablename__ = "cliente"

    id_cliente = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuario.id_user"), nullable=False)
    nombre_cli = Column(String(100), nullable=False)
    apellido_cli = Column(String(100), nullable=False)
    cedula = Column(String(20), unique=True, nullable=False)

    usuario = relationship("Usuario", back_populates="cliente")
    asistencias = relationship("ControlAcceso", back_populates="cliente")
    reservas = relationship("Reserva", back_populates="cliente")
    membresias = relationship("Membresia", back_populates="cliente")
    evaluaciones = relationship("EvaluacionBiometrica", back_populates="cliente")
    pagos = relationship("PagoMembresia", back_populates="cliente")
    compras = relationship("VentaProducto", back_populates="cliente")
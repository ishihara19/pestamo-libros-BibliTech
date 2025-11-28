from sqlalchemy import Column, Integer, String, DateTime, BigInteger, ForeignKey, Date
from sqlalchemy.orm import relationship
from ..core.db.postgre import Base
from sqlalchemy.sql import func

from .ejemplar import Ejemplar
from .usuario import Usuario

class Prestamo(Base):
    __tablename__ = "prestamo"

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    ejemplar_id = Column(Integer, ForeignKey("ejemplar.id"), nullable=False)
    fecha_solicitud = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    fecha_entrega = Column(Date, nullable=True, index=True)
    fecha_prevista_devolucion = Column(Date, nullable=False, index=True)
    fecha_devuelto = Column(DateTime(timezone=True), nullable=True)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
    actualizado_en = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relaciones
    ejemplar = relationship("Ejemplar", back_populates="prestamo")
    usuarios = relationship("Usuario", back_populates="prestamo")
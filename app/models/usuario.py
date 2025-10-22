from sqlalchemy import Column, Integer, String, DateTime, BigInteger, ForeignKey, Date
from sqlalchemy.orm import relationship
from ..core.db.postgre import Base
from sqlalchemy.sql import func

from .rol import Rol
from .tipo_documento import TipoDocumento
from .estado import Estado

class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    correo = Column(String(50), unique=True, nullable=False)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(100), nullable=False)
    documento = Column(String(20), unique=True, nullable=False)
    contrasena = Column(String(100), nullable=False)
    tipo_documento_id = Column(Integer, ForeignKey("tipo_documento.id"), nullable=False)
    estado_id = Column(Integer, ForeignKey("estado.id"), nullable=False, server_default="2")
    rol_id = Column(Integer, ForeignKey("rol.id"), nullable=False)
    token = Column(String(6), nullable=True)
    telefono = Column(String(20), nullable=True)
    direccion = Column(String(200), nullable=True)
    fecha_nacimiento = Column(Date, nullable=True)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
    actualizado_en = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # 👇 Relaciones nuevas
    rol = relationship("Rol", back_populates="usuarios")
    tipo_documento = relationship("TipoDocumento", back_populates="usuarios")
    estado = relationship("Estado", back_populates="usuarios")
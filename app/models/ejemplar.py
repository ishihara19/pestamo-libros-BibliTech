from sqlalchemy import Column, Integer, String, DateTime, BigInteger, ForeignKey, Date
from sqlalchemy.orm import relationship
from ..core.db.postgre import Base
from sqlalchemy.sql import func

from .libro import Libro
from .estado import Estado

class Ejemplar(Base):
    __tablename__ = "ejemplar"

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    codigo_interno = Column(String(50), unique=True, nullable=False, index=True)
    libro_id = Column(Integer, ForeignKey("libro.id"), nullable=False)
    estado_id = Column(Integer, ForeignKey("estado.id"), nullable=False, server_default="1")
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
    fecha_adquisicion = Column(Date, nullable=False, index=True)
    actualizado_en = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relaciones
    libro = relationship("Libro", back_populates="ejemplar")
    estado = relationship("Estado", back_populates="ejemplar")
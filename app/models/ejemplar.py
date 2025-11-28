from sqlalchemy import Column, Integer, String, DateTime, BigInteger, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.db.postgre import Base
from ..core.config import settings


from .libro import Libro
from .estado import Estado

class Ejemplar(Base):
    __tablename__ = "ejemplar"

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    codigo_interno = Column(String(50), unique=True, nullable=False, index=True)
    libro_id = Column(Integer, ForeignKey("libro.id"), nullable=False)
    estado_id = Column(Integer, ForeignKey("estado.id"), nullable=False, server_default=str(settings.DISPONIBILIDAD_EJEMPLAR_DISPONIBLE_ID))
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
    fecha_adquisicion = Column(Date, nullable=False, index=True)
    actualizado_en = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relaciones
    libro = relationship("Libro", back_populates="ejemplar")
    estado = relationship("Estado", back_populates="ejemplar")
    prestamo = relationship("Prestamo", back_populates="ejemplar")
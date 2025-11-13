from sqlalchemy import Column, Integer, String, text, DateTime,ForeignKey,Text
from ..core.db.postgre import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .categoria import Categoria

class Libro(Base):
    __tablename__ = 'libro'
    
    id = Column(Integer, primary_key=True, server_default=text("nextval('libro_id_seq'::regclass)"), index=True)
    titulo = Column(String(100), nullable=False, index=True)
    descripcion = Column(String(1000), nullable=True)
    categoria_id = Column(Integer, ForeignKey("categoria.id"), nullable=False)
    editorial = Column(String(100), nullable=True)
    fecha_publicacion = Column(DateTime(timezone=True), nullable=True)
    creado_en = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    actualizado_en = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    imagen_url = Column(Text, nullable=False)

    # Relaciones
    categoria = relationship("Categoria", back_populates="libros")
    ejemplar = relationship("Ejemplar", back_populates="libro")
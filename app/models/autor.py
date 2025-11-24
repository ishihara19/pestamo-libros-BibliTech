from sqlalchemy import Column, Integer, String, text, DateTime, Date
from ..core.db.postgre import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .autor_libro import autor_libro

class Autor(Base):
    __tablename__ = 'autor'
    
    id = Column(Integer, primary_key=True, server_default=text("nextval('autor_id_seq'::regclass)"), index=True)
    nombre = Column(String(100), nullable=False, index=True)
    apellido = Column(String(100), nullable=False, index=True)
    fecha_nacimiento = Column(Date, nullable=True)
    nacionalidad = Column(String(50), nullable=True, index=True)
    creado_en = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    actualizado_en = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    # Relación many-to-many con libros a través de autor_libro
    libros = relationship("Libro", secondary=autor_libro, back_populates="autores")
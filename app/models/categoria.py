from sqlalchemy import Column, Integer, String, text, DateTime
from ..core.db.postgre import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Categoria(Base):
    __tablename__ = 'categoria'

    id = Column(Integer, primary_key=True, server_default=text("nextval('categoria_id_seq'::regclass)"), index=True)
    nombre = Column(String(100), nullable=False, index=True)
    descripcion = Column(String(1000), nullable=True)
    creado_en = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    actualizado_en = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    libros = relationship("Libro", back_populates="categoria")
from sqlalchemy import Column, Integer, String, text, DateTime
from ..core.db.postgre import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Estado(Base):
    __tablename__ = 'estado'
    
    id = Column(Integer, primary_key=True, server_default=text("nextval('estado_id_seq'::regclass)"), index=True)
    nombre = Column(String(50), nullable=False)
    descripcion = Column(String(300), nullable=True)
    tipo = Column(String(50), nullable=False)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
    actualizado_en = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    usuarios = relationship("Usuario", back_populates="estado")
from sqlalchemy import Column, Integer, String, text, DateTime
from ..core.db.postgre import Base
from sqlalchemy.sql import func


class TipoDocumento(Base):
    __tablename__ = 'tipo_documento'
    
    id = Column(Integer, primary_key=True, server_default=text("nextval('tipo_documento_id_seq'::regclass)"), index=True)
    nombre = Column(String(50), nullable=False)
    acronimo = Column(String(50), nullable=False)
    descripcion = Column(String(300), nullable=True)
    creado_en = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    actualizado_en = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
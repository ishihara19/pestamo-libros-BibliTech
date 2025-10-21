from sqlalchemy import Column, Integer, String, text, select, BigInteger, DateTime, Date
from ..core.db.postgre import Base

class Estado(Base):
    __tablename__ = 'estado'
    
    id = Column(Integer, primary_key=True, server_default=text("nextval('estado_id_seq'::regclass)"), index=True)
    nombre = Column(String(50), nullable=False)
    descripcion = Column(String(300), nullable=True)
    tipo = Column(String(50), nullable=False)
    creado_en = Column(DateTime(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    actualizado_en = Column(DateTime(timezone=True), nullable=True, server_default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP"))
    
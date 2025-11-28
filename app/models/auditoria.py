from sqlalchemy import Column, Text, DateTime, BigInteger, JSON
from sqlalchemy.dialects.postgresql import INET
from ..core.db.postgre import Base

class Auditoria(Base):
    __tablename__ = "log_auditoria"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    tabla = Column(Text, nullable=False, index=True)
    operacion = Column(Text, nullable=False, index=True)
    usuario_db = Column(Text, nullable=False, index=True)
    usuario_app = Column(Text, nullable=True, index=True)
    ip = Column(INET, nullable=False, index=True)
    host = Column(Text, nullable=False, index=True)
    operacion_app = Column(Text, nullable=True, index=True)
    fecha_operacion = Column(DateTime(timezone=True), index=True, nullable=False)
    datos_anteriores = Column(JSON, nullable=True)
    datos_nuevos = Column(JSON, nullable=True)
from sqlalchemy import Column, Integer, String, text, DateTime
from ..core.db.postgre import Base
from sqlalchemy.sql import func

class Rol(Base):
    __tablename__ = "rol"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    acronimo = Column(String(50), nullable=False)
    descripcion = Column(String(300), nullable=True)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
    actualizado_en = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
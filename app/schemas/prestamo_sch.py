from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, date
from typing import Optional
from ..utils.tiempo_tz import to_localtime

class HacerPrestamo(BaseModel):
    
    usuario_id: int = Field(..., description="ID del usuario que realiza el préstamo")
    ejemplar_id: int = Field(..., description="ID del ejemplar que se presta")
    fecha_solicitud: datetime = Field(..., description="Fecha en que se realiza el préstamo")
    
class ValidarPrestamo(BaseModel):
    
    documento: str = Field(..., description="Documento del usuario que realiza el préstamo")
     

class ValidarPrestamoResponse(BaseModel):
    nombre_usuario: str
    apellido_usuario: str
    correo_usuario: str
    titulo_libro: str
    codigo_interno_ejemplar: str
    fecha_solicitud: datetime
    fecha_prevista_devolucion: date   
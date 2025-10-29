from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import datetime
from ipaddress import IPv4Address
from typing import Optional
from ..utils.tiempo_tz import to_localtime
from ..utils.utils import normalizar_nombre_propio

class AuditoriaView(BaseModel):
    id: int
    tabla: str
    operacion: str
    usuario_db: str
    usuario_app: str
    ip: str | IPv4Address
    host: str
    operacion_app: Optional[str]
    fecha_operacion: datetime
    datos_anteriores: dict
    datos_nuevos: dict

    class Config:
       from_attributes = True
        
    @classmethod
    def model_validate(cls, obj) -> 'AuditoriaView':
        instance = super().model_validate(obj)
        # Solo convertir para mostrar
        instance.fecha_operacion = to_localtime(instance.fecha_operacion)
        return instance



    

   
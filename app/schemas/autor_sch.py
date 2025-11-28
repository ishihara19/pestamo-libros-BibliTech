from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import datetime, date
from typing import Optional
from ..utils.tiempo_tz import to_localtime
from ..utils.utils import normalizar_nombre_propio

class AutorBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=50)
    apellido: str = Field(..., min_length=2, max_length=50)
    fecha_nacimiento: date
    nacionalidad: str = Field(..., min_length=2, max_length=50)
    
    @field_validator("nombre", "apellido")
    @classmethod
    def validar_y_normalizar_nombre(cls, v: str) -> str:
        return normalizar_nombre_propio(v)



class AutorCreate(AutorBase):
    pass

class AutorUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=50)
    apellido: Optional[str] = Field(None, min_length=2, max_length=50)
    fecha_nacimiento: Optional[datetime]
    nacionalidad: Optional[str] = Field(None, min_length=2, max_length=50)
    
    @field_validator("nombre", "apellido")
    @classmethod
    def validar_y_normalizar_nombre(cls, v: str) -> str:
        if v is None:
            return v        
        return normalizar_nombre_propio(v)


class AutorView(AutorBase):
    id: int
    creado_en: datetime
    actualizado_en: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def model_validate(cls, obj) -> 'AutorView':
        instance = super().model_validate(obj)
        # Solo convertir para mostrar
        instance.creado_en = to_localtime(instance.creado_en)
        instance.actualizado_en = to_localtime(instance.actualizado_en)
        return instance

class AutorSimpleView(BaseModel):
    id: int
    nombre: str
    apellido: str
    nacionalidad: str
    
    model_config = ConfigDict(from_attributes=True)            

    
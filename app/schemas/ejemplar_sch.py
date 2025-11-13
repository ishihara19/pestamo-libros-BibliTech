from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, date
from typing import Optional
from ..utils.tiempo_tz import to_localtime

class EjemplarBase(BaseModel):
    
    libro_id: int = Field(..., description="ID del libro asociado al ejemplar")
    estado_id: Optional[int] = Field(1, description="ID del estado del ejemplar")    
    fecha_adquisicion: date = Field(..., description="Fecha de adquisición del ejemplar")
    
class EjemplarCreate(EjemplarBase):
    pass

class EjemplarUpdate(BaseModel):
    libro_id: Optional[int] = Field(None, description="ID del libro asociado al ejemplar")
    estado_id: Optional[int] = Field(None, description="ID del estado del ejemplar")
    codigo_interno: Optional[str] = Field(None, max_length=50, description="Código interno único del ejemplar")
    fecha_adquisicion: Optional[date] = Field(None, description="Fecha de adquisición del ejemplar")
    
class EjemplarView(EjemplarBase):
    id: int
    creado_en: datetime
    actualizado_en: Optional[datetime]
    codigo_interno: Optional[str]
    

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def model_validate(cls, obj) -> 'EjemplarView':
        instance = super().model_validate(obj)
        # Solo convertir para mostrar
        instance.creado_en = to_localtime(instance.creado_en)
        instance.actualizado_en = to_localtime(instance.actualizado_en) if instance.actualizado_en else None
        return instance

class EjemplarReaderNormalized(BaseModel):
    id: int
    codigo_interno: str
    libro_titulo: str
    estado_nombre: str
    fecha_adquisicion: date
    creado_en: datetime
    actualizado_en: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_model(cls, ejemplar):
        return cls(
            id=ejemplar.id,
            codigo_interno=ejemplar.codigo_interno,
            libro_titulo=ejemplar.libro.titulo if ejemplar.libro else None,
            estado_nombre=ejemplar.estado.nombre if ejemplar.estado else None,
            fecha_adquisicion=ejemplar.fecha_adquisicion,
            creado_en=ejemplar.creado_en,
            actualizado_en=ejemplar.actualizado_en,
        )

class EjemplarUpdateEstado(BaseModel):
    estado_id: int
    actualizado_en: Optional[datetime]
                        
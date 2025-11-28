from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional
from ..utils.tiempo_tz import to_localtime

class TipoDocumentoBase(BaseModel):
    nombre: str = Field(..., max_length=50)
    acronimo: str = Field(..., max_length=50)
    descripcion: Optional[str] = Field(None, max_length=300)

class TipoDocumentoCreate(TipoDocumentoBase):
    pass

class TipoDocumentoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=50)
    acronimo: Optional[str] = Field(None, max_length=50)
    descripcion: Optional[str] = Field(None, max_length=300)

class TipoDocumentoView(TipoDocumentoBase):
    id: int
    creado_en: datetime
    actualizado_en: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
    @classmethod
    def model_validate(cls, obj) -> 'TipoDocumentoView':
        instance = super().model_validate(obj)
        # Solo convertir para mostrar
        instance.creado_en = to_localtime(instance.creado_en)
        instance.actualizado_en = to_localtime(instance.actualizado_en)
        return instance        
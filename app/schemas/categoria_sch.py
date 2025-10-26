from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional
from ..utils.tiempo_tz import to_localtime

class CatengoriaBase(BaseModel):
    nombre: str = Field(..., max_length=100)
    descripcion: Optional[str] = Field(None, max_length=300)
 

class CategoriaCreate(CatengoriaBase):
    pass

class CategoriaUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=300)
    
class CategoriaView(CatengoriaBase):
    id: int
    creado_en: datetime
    actualizado_en: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
    @classmethod
    def model_validate(cls, obj) -> 'CategoriaView':
        instance = super().model_validate(obj)
        # Solo convertir para mostrar
        instance.creado_en = to_localtime(instance.creado_en)
        instance.actualizado_en = to_localtime(instance.actualizado_en)
        return instance            
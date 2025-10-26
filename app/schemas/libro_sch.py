from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional
from ..utils.tiempo_tz import to_localtime

class LibroBase(BaseModel):
    titulo: str = Field(..., max_length=100)
    descripcion: str = Field(..., max_length=1000)
    categoria_id: int
    editorial: str = Field(..., max_length=100)
    fecha_publicacion: datetime = Field(...)

class LibroCreate(LibroBase):
    pass

class LibroUpdate(BaseModel):
    titulo: Optional[str] = Field(None, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=1000)
    categoria_id: Optional[int]
    editorial: Optional[str] = Field(None, max_length=100)
    fecha_publicacion: Optional[datetime] = Field(None)

class LibroView(LibroBase):
    id: int
    creado_en: datetime
    actualizado_en: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def model_validate(cls, obj) -> 'LibroView':
        instance = super().model_validate(obj)
        # Solo convertir para mostrar
        instance.creado_en = to_localtime(instance.creado_en)
        instance.actualizado_en = to_localtime(instance.actualizado_en)
        return instance

class LibroViewNormalized(BaseModel):
    id: int
    titulo: str
    descripcion: Optional[str]
    categoria: Optional[str]
    editorial: Optional[str]
    creado_en: datetime
    actualizado_en: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def model_validate(cls, obj) -> "LibroViewNormalized":
        instance = super().model_validate(obj)
        # Solo convertir para mostrar (proteger None)
        instance.creado_en = to_localtime(instance.creado_en)
        if instance.actualizado_en is not None:
            instance.actualizado_en = to_localtime(instance.actualizado_en)
        return instance

    @classmethod
    def from_model(cls, libro):
        return cls(
            id=libro.id,
            titulo=libro.titulo,
            descripcion=libro.descripcion,
            categoria=libro.categoria.nombre if getattr(libro, "categoria", None) else None,
            editorial=libro.editorial,
            creado_en=libro.creado_en,
            actualizado_en=libro.actualizado_en,
        )
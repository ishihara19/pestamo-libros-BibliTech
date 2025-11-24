from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, date
from typing import Optional
from typing import List
from ..utils.tiempo_tz import to_localtime
from .autor_sch import AutorSimpleView

class LibroBase(BaseModel):
    titulo: str = Field(..., max_length=100)
    descripcion: str = Field(..., max_length=1000)
    categoria_id: int
    editorial: str = Field(..., max_length=100)
    fecha_publicacion: date = Field(...)

class LibroCreate(LibroBase):
    autores_ids: Optional[List[int]] = None

class LibroUpdate(BaseModel):
    titulo: Optional[str] = Field(None, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=1000)
    categoria_id: Optional[int]
    editorial: Optional[str] = Field(None, max_length=100)
    fecha_publicacion: Optional[date] = Field(None)
    imagen_url: Optional[str] = Field(None)
    autores_ids: Optional[List[int]] = None
    
class LibroView(LibroBase):
    id: int
    creado_en: datetime
    actualizado_en: Optional[datetime]
    imagen_url: Optional[str] = Field(None)
    autores: list[AutorSimpleView] = []
    ejemplares_count: int = 0
    ejemplares_disponibles: int = 0
    ejemplares_reservados: int = 0
    ejemplares_prestados: int = 0
    ejemplares_danados: int = 0
    
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
    fecha_publicacion: Optional[date]
    actualizado_en: Optional[datetime]
    imagen_url: Optional[str]
    autores: list[AutorSimpleView] = []
    ejemplares_count: int = 0
    ejemplares_disponibles: int = 0
    ejemplares_reservados: int = 0
    ejemplares_prestados: int = 0
    ejemplares_danados: int = 0

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
            fecha_publicacion=libro.fecha_publicacion,
            imagen_url=libro.imagen_url,
            creado_en=libro.creado_en,
            actualizado_en=libro.actualizado_en,
            autores=[AutorSimpleView.model_validate(a) for a in getattr(libro, "autores", [])],
            ejemplares_count=len(getattr(libro, "ejemplar", []) or []),
            ejemplares_disponibles=sum(1 for e in getattr(libro, "ejemplar", []) if getattr(e, "estado_id", None) == 3),
            ejemplares_reservados=sum(1 for e in getattr(libro, "ejemplar", []) if getattr(e, "estado_id", None) == 4),
            ejemplares_prestados=sum(1 for e in getattr(libro, "ejemplar", []) if getattr(e, "estado_id", None) == 5),
            ejemplares_danados=sum(1 for e in getattr(libro, "ejemplar", []) if getattr(e, "estado_id", None) == 6),
        )
        

class LibroURLUpdate(BaseModel):
    imagen_url: str        
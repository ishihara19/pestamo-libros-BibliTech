from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, date
from typing import Optional
from ..utils.tiempo_tz import to_localtime
from pydantic import field_validator


class HacerPrestamo(BaseModel):

    libro_id: int = Field(..., description="ID del libro que se presta")
    fecha_solicitud: datetime = Field(
        ..., description="Fecha en que se realiza el préstamo"
    )
    dias_prestamo: int = Field(..., description="Días de préstamo solicitados")


class PrestamoViewBibliotecario(BaseModel):

    id: int
    usuario_id: int
    ejemplar_id: int
    fecha_solicitud: datetime
    fecha_prevista_devolucion: date
    fecha_entrega: Optional[date]
    fecha_devuelto: Optional[date]
    creado_en: datetime
    actualizado_en: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def model_validate(cls, obj) -> "PrestamoViewBibliotecario":
        instance = super().model_validate(obj)
        # Solo convertir para mostrar
        instance.fecha_solicitud = to_localtime(instance.fecha_solicitud)
        instance.creado_en = to_localtime(instance.creado_en)
        instance.actualizado_en = to_localtime(instance.actualizado_en)
        return instance


class PrestamoViewNormalizedBibliotecario(BaseModel):
    usuario_nombre: str
    documento_usuario: str
    libro_titulo: str
    ejemplar_codigo_interno: str
    estado_ejemplar: str
    fecha_solicitud: datetime
    fecha_entrega: Optional[date]
    fecha_prevista_devolucion: date
    fecha_devuelto: Optional[datetime]
    creado_en: datetime
    actualizado_en: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

    @field_validator(
        "fecha_solicitud",
        "fecha_devuelto",
        "creado_en",
        "actualizado_en",
        mode="before",
    )
    def convert_to_localtime(cls, value):
        if value and isinstance(value, datetime):
            return to_localtime(value)
        return value

    @classmethod
    def from_model(cls, prestamo):
        return cls(
            documento_usuario=prestamo.usuarios.documento,
            fecha_solicitud=prestamo.fecha_solicitud,
            fecha_prevista_devolucion=prestamo.fecha_prevista_devolucion,
            fecha_entrega=prestamo.fecha_entrega,
            fecha_devuelto=prestamo.fecha_devuelto,
            creado_en=prestamo.creado_en,
            actualizado_en=prestamo.actualizado_en,
            usuario_nombre=f"{prestamo.usuarios.nombre} {prestamo.usuarios.apellido}",
            libro_titulo=prestamo.ejemplar.libro.titulo,
            ejemplar_codigo_interno=prestamo.ejemplar.codigo_interno,
            estado_ejemplar=prestamo.ejemplar.estado.nombre,
        )


class PrestamoViewNormalizedLector(BaseModel):
    libro_titulo: str
    ejemplar_codigo_interno: str
    estado_ejemplar: str

    fecha_solicitud: datetime
    fecha_entrega: Optional[date]
    fecha_prevista_devolucion: date
    fecha_devuelto: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

    @field_validator("fecha_solicitud", "fecha_devuelto", mode="before")
    def convert_to_localtime(cls, value):
        if value and isinstance(value, datetime):
            return to_localtime(value)
        return value

    @classmethod
    def from_model(cls, prestamo):
        return cls(
            fecha_solicitud=prestamo.fecha_solicitud,
            fecha_prevista_devolucion=prestamo.fecha_prevista_devolucion,
            fecha_entrega=prestamo.fecha_entrega,
            fecha_devuelto=prestamo.fecha_devuelto,
            libro_titulo=prestamo.ejemplar.libro.titulo,
            ejemplar_codigo_interno=prestamo.ejemplar.codigo_interno,
            estado_ejemplar=prestamo.ejemplar.estado.nombre,
        )


class ConfirmarEntregaPrestamo(BaseModel):
    numero_documento: str = Field(..., description="Número de documento del usuario")
    ejemplar_codigo_interno: str = Field(..., description="Código interno del ejemplar")

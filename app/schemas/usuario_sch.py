from pydantic import BaseModel, ConfigDict, Field, field_validator, EmailStr,ValidationInfo
from datetime import date, datetime
from typing import Optional
import re

from ..utils.tiempo_tz import to_localtime
from ..utils.utils import (
    normalizar_correo,
    validar_complejidad_contrasena,
    tiene_edad_minima,
    normalizar_nombre_propio,
    validar_tipo_documento_edad,
)


class UsuarioBase(BaseModel):
    correo: EmailStr = Field(..., min_length=5, max_length=100)
    nombre: str = Field(..., min_length=2, max_length=50)
    apellido: str = Field(..., min_length=2, max_length=50)
    documento: str = Field(..., max_length=30)
    tipo_documento_id: int
    estado_id: int
    rol_id: int
    telefono: Optional[str] = Field(None, max_length=10)
    direccion: Optional[str] = Field(None, max_length=200)
    fecha_nacimiento: date = Field(...)


class UsuarioCreate(BaseModel):
    correo: EmailStr = Field(..., max_length=100)
    nombre: str = Field(..., max_length=50)
    apellido: str = Field(..., max_length=50)
    documento: str = Field(..., max_length=30)
    tipo_documento_id: int
    telefono: str = Field(..., min_length=10, max_length=10)
    direccion: Optional[str] = Field(None, min_length=8, max_length=200)
    fecha_nacimiento: date = Field(...)
    contrasena: str = Field(..., min_length=8, max_length=255)

    @field_validator("nombre", "apellido")
    @classmethod
    def validar_y_normalizar_nombre(cls, v: str) -> str:
        return normalizar_nombre_propio(v)

    @field_validator("fecha_nacimiento")
    @classmethod
    def validar_fecha_nacimiento(cls, v: date, info: ValidationInfo) -> date:
        """Valida edad mínima y coherencia con tipo_documento_id si está presente."""
        if not tiene_edad_minima(v, 9):
            raise ValueError("El usuario debe tener al menos 9 años.")
        
        tipo_documento = info.data.get("tipo_documento_id")
        if tipo_documento:
            validar_tipo_documento_edad(tipo_documento, v)
        
        return v
    @field_validator("correo")
    @classmethod
    def validar_y_normalizar_correo(cls, v: str) -> str:
        return normalizar_correo(v)

    @field_validator("contrasena")
    @classmethod
    def password_complexity(cls, v: str) -> str:
        return validar_complejidad_contrasena(v)


class UsuarioUpdateAdmin(BaseModel):
    correo: Optional[EmailStr] = None
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    documento: Optional[str] = None
    contrasena: Optional[str] = None
    tipo_documento_id: Optional[int] = None
    estado_id: Optional[int] = None
    rol_id: Optional[int] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    fecha_nacimiento: Optional[date] = None

    @field_validator("nombre", "apellido")
    @classmethod
    def validar_y_normalizar_nombre(cls, v: str) -> str:
        return normalizar_nombre_propio(v)

    @field_validator("fecha_nacimiento")
    @classmethod
    def validar_fecha_nacimiento(cls, v: date) -> date:
        if not tiene_edad_minima(v, 9):
            raise ValueError("El usuario debe tener al menos 9 años.")
        return v

    @field_validator("correo")
    @classmethod
    def validar_y_normalizar_correo(cls, v: str) -> str:
        return normalizar_correo(v)

    @field_validator("contrasena")
    @classmethod
    def password_complexity(cls, v: str) -> str:
        return validar_complejidad_contrasena(v)


class UsuarioUpdatePerfil(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=50)
    apellido: Optional[str] = Field(None, min_length=2, max_length=50)
    telefono: Optional[str] = Field(None, min_length=10, max_length=10)
    direccion: Optional[str] = Field(None, min_length=8, max_length=200)
    fecha_nacimiento: Optional[date] = Field(None)

    @field_validator("nombre", "apellido")
    @classmethod
    def validar_y_normalizar_nombre(cls, v: str) -> str:
        return normalizar_nombre_propio(v)

    @field_validator("fecha_nacimiento")
    @classmethod
    def validar_fecha_nacimiento(cls, v: date) -> date:
        if not tiene_edad_minima(v, 9):
            raise ValueError("El usuario debe tener al menos 9 años.")
        return v


class UsuarioUpdateContrasena(BaseModel):
    contrasena_actual: str = Field(..., min_length=8, max_length=255)
    contrasena_nueva: str = Field(..., min_length=8, max_length=255)

    @field_validator("contrasena_nueva")
    @classmethod
    def password_complexity(cls, v: str) -> str:
        return validar_complejidad_contrasena(v)


class UsuarioLogin(BaseModel):
    correo: EmailStr = Field(..., max_length=100)
    contrasena: str = Field(..., min_length=8, max_length=255)

    @field_validator("correo")
    @classmethod
    def validar_y_normalizar_correo(cls, v: str) -> str:
        """Aplica normalización al correo electrónico."""
        return normalizar_correo(v)


class UsuarioResetearContrasena(BaseModel):
    correo: EmailStr = Field(..., max_length=100)

    @field_validator("correo")
    @classmethod
    def validar_y_normalizar_correo(cls, v: str) -> str:
        """Aplica normalización al correo electrónico."""
        return normalizar_correo(v)


class UsuarioVerificarToken(BaseModel):
    correo: EmailStr = Field(..., max_length=100)
    token: str = Field(..., max_length=100)
    contrasena_nueva: str = Field(..., min_length=8, max_length=255)

    @field_validator("correo")
    @classmethod
    def validar_y_normalizar_correo(cls, v: str) -> str:
        """Aplica normalización al correo electrónico."""
        return normalizar_correo(v)

    @field_validator("contrasena_nueva")
    @classmethod
    def password_complexity(cls, v: str) -> str:
        return validar_complejidad_contrasena(v)


class UsuarioCambiarEstadoAdmin(BaseModel):
    estado_id: int


class UsuarioCambiarRolAdmin(BaseModel):
    rol_id: int


class UsuarioView(UsuarioBase):
    id: int
    creado_en: datetime
    actualizado_en: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def model_validate(cls, obj) -> "UsuarioView":
        instance = super().model_validate(obj)
        # Solo convertir para mostrar
        instance.creado_en = to_localtime(instance.creado_en)
        instance.actualizado_en = to_localtime(instance.actualizado_en)
        return instance


class UsuarioReadNormalized(BaseModel):
    id: int
    correo: str
    nombre: str
    apellido: str
    documento: str
    tipo_documento: str
    rol: str
    estado: str
    telefono: str | None
    direccion: str | None
    fecha_nacimiento: date | None
    creado_en: datetime
    actualizado_en: datetime | None

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_model(cls, usuario):
        return cls(
            id=usuario.id,
            correo=usuario.correo,
            nombre=usuario.nombre,
            apellido=usuario.apellido,
            documento=usuario.documento,
            tipo_documento=(
                usuario.tipo_documento.acronimo if usuario.tipo_documento else None
            ),
            rol=usuario.rol.acronimo if usuario.rol else None,
            estado=usuario.estado.nombre if usuario.estado else None,
            telefono=usuario.telefono,
            direccion=usuario.direccion,
            fecha_nacimiento=usuario.fecha_nacimiento,
            creado_en=usuario.creado_en,
            actualizado_en=usuario.actualizado_en,
        )


class UsuarioMensaje(BaseModel):
    message: str

from pydantic import BaseModel, ConfigDict, Field, field_validator, EmailStr
from datetime import date, datetime
from typing import Optional
import re

from ..utils.tiempo_tz import to_localtime
from ..utils.utils import normalizar_correo, validar_complejidad_contrasena


class UsuarioBase(BaseModel):
    correo: EmailStr = Field(..., max_length=100)
    nombre: str = Field(..., max_length=50)
    apellido: str = Field(..., max_length=50)
    documento: str = Field(..., max_length=30)
    tipo_documento_id: int
    estado_id: int
    rol_id: int
    telefono: Optional[str] = Field(None, max_length=10)
    direccion: Optional[str] = Field(None, max_length=200)
    fecha_nacimiento: Optional[date] = None
    
    @field_validator("correo")
    @classmethod
    def validar_y_normalizar_correo(cls, v: str) -> str:
        """Aplica normalización al correo electrónico."""
        return normalizar_correo(v)    

class UsuarioCreate(UsuarioBase):
    contrasena: str = Field(..., min_length=8, max_length=255)
    
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
    
    @field_validator("correo")
    @classmethod
    def validar_y_normalizar_correo(cls, v: str) -> str:
        """Aplica normalización al correo electrónico."""
        return normalizar_correo(v)

class UsuarioUpdatePerfil(BaseModel):    
    nombre: Optional[str] = None
    apellido: Optional[str] = None    
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    
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
    def model_validate(cls, obj) -> 'UsuarioView':
        instance = super().model_validate(obj)
        # Solo convertir para mostrar
        instance.creado_en = to_localtime(instance.creado_en)
        instance.actualizado_en = to_localtime(instance.actualizado_en)
        return instance   

class UsuarioMensaje(BaseModel):
    message: str   
    
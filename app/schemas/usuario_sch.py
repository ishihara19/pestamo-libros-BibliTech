from pydantic import BaseModel, ConfigDict, Field, field_validator, EmailStr
from datetime import date, datetime
from typing import Optional
from ..utils.tiempo_tz import to_localtime
import re


class UsuarioBase(BaseModel):
    correo: EmailStr = Field(..., max_length=50)
    nombre: str = Field(..., max_length=100)
    apellido: str = Field(..., max_length=100)
    documento: str = Field(..., max_length=20)
    tipo_documento_id: int
    estado_id: int
    rol_id: int
    telefono: Optional[str] = Field(None, max_length=10)
    direccion: Optional[str] = Field(None, max_length=200)
    fecha_nacimiento: Optional[date] = None

class UsuarioCreate(UsuarioBase):
    contrasena: str = Field(..., min_length=8, max_length=100)

    @field_validator("contrasena")
    @classmethod
    def password_complexity(cls, v: str) -> str:
        """Valida la complejidad de la contraseña."""
        if not re.search(r"[a-z]", v):
            raise ValueError("La contraseña debe contener al menos una letra minúscula")
        if not re.search(r"[A-Z]", v):
            raise ValueError("La contraseña debe contener al menos una letra mayúscula")
        if not re.search(r"[0-9]", v):
            raise ValueError("La contraseña debe contener al menos un número")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError(
                "La contraseña debe contener al menos un carácter especial"
            )
        return v    

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

class UsuarioUpdatePerfil(BaseModel):    
    nombre: Optional[str] = None
    apellido: Optional[str] = None    
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    
class UsuarioUpdateContrasena(BaseModel):
    contrasena_actual: str = Field(..., min_length=8, max_length=100)
    contrasena_nueva: str = Field(..., min_length=8, max_length=100)
    @field_validator("contrasena_nueva")
    @classmethod
    def password_complexity(cls, v: str) -> str:
        """Valida la complejidad de la contraseña."""
        if not re.search(r"[a-z]", v):
            raise ValueError("La contraseña debe contener al menos una letra minúscula")
        if not re.search(r"[A-Z]", v):
            raise ValueError("La contraseña debe contener al menos una letra mayúscula")
        if not re.search(r"[0-9]", v):
            raise ValueError("La contraseña debe contener al menos un número")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError(
                "La contraseña debe contener al menos un carácter especial"
            )
        return v
class UsuarioLogin(BaseModel):
    correo: EmailStr = Field(..., max_length=50)
    contrasena: str = Field(..., min_length=8, max_length=100)

class UsuarioResetearContrasena(BaseModel):
    correo: EmailStr = Field(..., max_length=50)

class UsuarioVerificarToken(BaseModel):
    correo: EmailStr = Field(..., max_length=50)
    token: str = Field(..., max_length=100)
    contrasena_nueva: str = Field(..., min_length=8, max_length=100)

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
    
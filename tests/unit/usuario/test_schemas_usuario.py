from app.schemas.usuario_sch import UsuarioBase, UsuarioCreate
from datetime import date
import pytest

def test_usuario_base_valid():
    usuario = UsuarioBase(
        correo="test@example.com",
        nombre="Juan",
        apellido="Pérez",
        documento="123456",
        tipo_documento_id=1,
        estado_id=1,
        rol_id=1,
        telefono="3001234567",
        direccion="Calle 1",
        fecha_nacimiento=date(2000, 1, 1)
    )
    assert usuario.nombre == "Juan"
    assert usuario.apellido == "Pérez"

def test_usuario_create_nombre_normalizado():
    usuario = UsuarioCreate(
        correo="test@example.com",
        nombre="maria de la cruz",
        apellido="gomez",
        documento="654321",
        tipo_documento_id=1,
        telefono="3001234567",
        direccion="Calle 222",
        fecha_nacimiento=date(2000, 1, 1),
        contrasena="Abcdef1!"
    )
    assert usuario.nombre == "Maria de la Cruz"
    assert usuario.apellido == "Gomez"

def test_usuario_create_fecha_nacimiento_invalida():
    with pytest.raises(ValueError):
        UsuarioCreate(
            correo="test@example.com",
            nombre="Juan",
            apellido="Pérez",
            documento="123456",
            tipo_documento_id=1,
            telefono="3001234567",
            direccion="Calle 1",
            fecha_nacimiento=date(2020, 1, 1),
            contrasena="Abcdef1!"
        )

import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.usuario_service import UsuarioService
from app.schemas.usuario_sch import UsuarioCreate
from datetime import date

@pytest.mark.asyncio
async def test_create_usuario():
    db = AsyncMock()
    db.add = MagicMock()
    db.commit = AsyncMock()
    db.refresh = AsyncMock()
    db.execute = AsyncMock()
    usuario_data = UsuarioCreate(
        correo="test@example.com",
        nombre="Juan",
        apellido="Pérez",
        documento="123456",
        tipo_documento_id=1,
        telefono="3001234567",
        direccion="Calle 123",
        fecha_nacimiento=date(2000, 1, 1),
        contrasena="Abcdef1!"
    )
    db.refresh.return_value = None
    # Mock para db.execute().scalar_one() que retorna un usuario completo
    class TipoDocumentoFake:
        acronimo = "DNI"
    class RolFake:
        acronimo = "ADMIN"
    class EstadoFake:
        nombre = "Activo"
    from datetime import datetime
    class UsuarioFake:
        id = 1
        correo = "test@example.com"
        nombre = "Juan"
        apellido = "Pérez"
        documento = "123456"
        tipo_documento = TipoDocumentoFake()
        rol = RolFake()
        estado = EstadoFake()
        telefono = "3001234567"
        direccion = "Calle 123"
        fecha_nacimiento = date(2000, 1, 1)
        creado_en = datetime.now()
        actualizado_en = None
    class FakeResult:
        def scalar_one(self):
            return UsuarioFake()
    db.execute.return_value = FakeResult()
    # No se prueba la respuesta final porque depende de más lógica, pero se valida el flujo DB
    await UsuarioService.create_usuario(usuario_data, db, host="localhost", ip="127.0.0.1")
    db.add.assert_called()
    db.commit.assert_awaited()
    db.refresh.assert_awaited()

@pytest.mark.asyncio
async def test_create_usuario_mock():
    db = AsyncMock()
    db.add = MagicMock()
    db.commit = AsyncMock()
    db.refresh = AsyncMock()
    db.execute = AsyncMock()
    from datetime import date, datetime
    usuario_data = UsuarioCreate(
        nombre="Juan",
        apellido="Pérez",
        correo="test@example.com",
        documento="123456",
        contrasena="Abcdef1!",
        tipo_documento_id=1,
        estado_id=1,
        rol_id=1,
        telefono="3001234567",
        fecha_nacimiento=date(2000, 1, 1)
    )
    # Mock para db.execute().scalar_one() que retorna un usuario completo
    class TipoDocumentoFake:
        acronimo = "DNI"
    class RolFake:
        acronimo = "ADMIN"
    class EstadoFake:
        nombre = "Activo"
    class UsuarioFake:
        id = 1
        correo = "test@example.com"
        nombre = "Juan"
        apellido = "Pérez"
        documento = "123456"
        tipo_documento = TipoDocumentoFake()
        rol = RolFake()
        estado = EstadoFake()
        telefono = "3001234567"
        direccion = "Calle 123"
        fecha_nacimiento = date(2000, 1, 1)
        creado_en = datetime.now()
        actualizado_en = None
    class FakeResult:
        def scalar_one(self):
            return UsuarioFake()
    db.execute.return_value = FakeResult()
    result = await UsuarioService.create_usuario(usuario_data, db, host="localhost", ip="127.0.0.1", username="admin")
    db.add.assert_called()
    db.commit.assert_awaited()
    db.refresh.assert_awaited()

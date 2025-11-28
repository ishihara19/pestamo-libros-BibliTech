import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.prestamo_service import PrestamoService
from app.schemas.prestamo_sch import HacerPrestamo
from app.models.usuario import Usuario
from datetime import datetime

@pytest.mark.asyncio
async def test_crear_prestamo():
    db = AsyncMock()
    db.add = MagicMock()
    db.commit = AsyncMock()
    db.refresh = AsyncMock()
    db.execute = AsyncMock()
    usuario = Usuario(id=1, nombre="Juan", apellido="Pérez", correo="test@example.com", documento="123456", contrasena="Abcdef1!", tipo_documento_id=1, estado_id=1, rol_id=1)
    prestamo_data = HacerPrestamo(libro_id=1, fecha_solicitud=datetime(2023, 1, 1, 10, 0, 0), dias_prestamo=7)
    async def refresh_side_effect(obj):
        pass
    db.refresh.side_effect = refresh_side_effect
    # Mock para ejemplar_disponible_info
    class EjemplarRow:
        def __init__(self, id, codigo_interno):
            self.id = id
            self.codigo_interno = codigo_interno
    class FakeResult:
        def one_or_none(self):
            return EjemplarRow(10, "L0001-E001")
        def scalar_one_or_none(self):
            # Simula el resultado de select(Libro.titulo).where(Libro.id == prestamo_data.libro_id)
            return "Libro de Prueba"
    db.execute.return_value = FakeResult()
    # No se prueba la respuesta final porque depende de más lógica, pero se valida el flujo DB
    await PrestamoService.crear_prestamo(db, prestamo_data, usuario, ip="127.0.0.1", host="localhost", username="admin")
    db.add.assert_called()
    db.commit.assert_awaited()

import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.ejemplar_service import EjemplarService
from app.schemas.ejemplar_sch import EjemplarCreate, EjemplarUpdate, EjemplarUpdateEstado

@pytest.mark.asyncio
async def test_create_ejemplar():
    db = AsyncMock()
    db.add = MagicMock()
    db.commit = AsyncMock()
    db.refresh = AsyncMock()
    db.execute = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    db.execute.return_value = mock_result
    ejemplar_data = EjemplarCreate(libro_id=1, fecha_adquisicion="2020-01-01")
    # Se mockea la función de código único
    import app.utils.utils as utils
    utils.generar_codigo_unico = AsyncMock(return_value="A1")
    # Mockear los atributos requeridos por Pydantic
    from datetime import datetime, date
    def add_side_effect(obj):
        obj.id = 1
        obj.creado_en = datetime.now()
        obj.actualizado_en = datetime.now()
        obj.codigo_interno = "A1"
        obj.estado_id = 1
        obj.fecha_adquisicion = date(2020, 1, 1)
    db.add.side_effect = add_side_effect
    async def refresh_side_effect(obj):
        obj.id = 1
        obj.creado_en = datetime.now()
        obj.actualizado_en = datetime.now()
        obj.codigo_interno = "A1"
        obj.estado_id = 1
        obj.fecha_adquisicion = date(2020, 1, 1)
    db.refresh.side_effect = refresh_side_effect
    result = await EjemplarService.create_ejemplar(ejemplar_data, db)
    db.add.assert_called()
    db.commit.assert_awaited()
    db.refresh.assert_awaited()

@pytest.mark.asyncio
async def test_actualizar_estado_ejemplar_not_found():
    db = AsyncMock()
    db.execute.return_value.scalar_one_or_none.return_value = None
    with pytest.raises(Exception):
        await EjemplarService.actualizar_estado_ejemplar(1, EjemplarUpdateEstado(estado_id=2), db)

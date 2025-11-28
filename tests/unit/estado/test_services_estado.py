import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.estado_service import EstadoService
from app.schemas.estado_sch import EstadoCreate, EstadoUpdate

@pytest.mark.asyncio
async def test_create_estado():
    db = AsyncMock()
    db.add = MagicMock()
    db.commit = AsyncMock()
    db.refresh = AsyncMock()
    estado_data = EstadoCreate(nombre="Activo", descripcion="En uso", tipo="general")
    # Mockear los atributos requeridos por Pydantic
    from datetime import datetime
    def add_side_effect(obj):
        obj.id = 1
        obj.creado_en = datetime.now()
        obj.actualizado_en = datetime.now()
    db.add.side_effect = add_side_effect
    async def refresh_side_effect(obj):
        obj.id = 1
        obj.creado_en = datetime.now()
        obj.actualizado_en = datetime.now()
    db.refresh.side_effect = refresh_side_effect
    result = await EstadoService.create_estado(estado_data, db)
    db.add.assert_called()
    db.commit.assert_awaited()
    db.refresh.assert_awaited()

@pytest.mark.asyncio
async def test_actualizar_estado_not_found():
    db = AsyncMock()
    db.execute.return_value.scalar_one_or_none.return_value = None
    with pytest.raises(Exception):
        await EstadoService.actualizar_estado(1, EstadoUpdate(nombre="Inactivo"), db)

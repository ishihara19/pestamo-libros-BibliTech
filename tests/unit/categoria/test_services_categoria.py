import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.categoria_service import CategoriaService
from app.schemas.categoria_sch import CategoriaCreate, CategoriaUpdate

@pytest.mark.asyncio
async def test_create_categoria():
    db = AsyncMock()
    db.add = MagicMock()
    db.commit = AsyncMock()
    db.refresh = AsyncMock()
    db.execute = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    db.execute.return_value = mock_result
    categoria_data = CategoriaCreate(nombre="Novela", descripcion="Narrativa literaria")
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
    result = await CategoriaService.create_categoria(categoria_data, db)
    db.add.assert_called()
    db.commit.assert_awaited()
    db.refresh.assert_awaited()

@pytest.mark.asyncio
async def test_actualizar_categoria_not_found():
    db = AsyncMock()
    db.execute.return_value.scalar_one_or_none.return_value = None
    with pytest.raises(Exception):
        await CategoriaService.actualizar_categoria(1, CategoriaUpdate(nombre="Nueva"), db)

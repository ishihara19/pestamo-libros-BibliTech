import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.rol_service import RolService
from app.schemas.rol_sch import RolCreate, RolUpdate

@pytest.mark.asyncio
async def test_create_role():
    db = AsyncMock()
    db.add = MagicMock()
    db.commit = AsyncMock()
    db.refresh = AsyncMock()
    role_data = RolCreate(nombre="Admin", descripcion="Administrador", acronimo="ADM")
    from datetime import datetime
    def add_side_effect(obj):
        obj.id = 1
        obj.creado_en = datetime.now()
    db.add.side_effect = add_side_effect
    async def refresh_side_effect(obj):
        obj.id = 1
        obj.creado_en = datetime.now()
    db.refresh.side_effect = refresh_side_effect
    result = await RolService.create_role(role_data, db)
    db.add.assert_called()
    db.commit.assert_awaited()
    db.refresh.assert_awaited()

@pytest.mark.asyncio
async def test_actualizar_role_not_found():
    db = AsyncMock()
    db.execute.return_value.scalar.return_value = None
    with pytest.raises(Exception):
        await RolService.actualizar_role(1, RolUpdate(nombre="Nuevo"), db)

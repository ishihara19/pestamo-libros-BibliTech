import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.autor_service import AutorService
from app.schemas.autor_sch import AutorCreate, AutorUpdate

@pytest.mark.asyncio
async def test_create_autor():
    db = AsyncMock()
    from datetime import date
    autor_data = AutorCreate(nombre="Gabriel", apellido="García", fecha_nacimiento=date(1927, 3, 6), nacionalidad="Colombiana")
    db.add = AsyncMock()
    db.commit = AsyncMock()
    from datetime import datetime
    async def refresh_side_effect(obj):
        obj.id = 1
        obj.creado_en = datetime.now()
    db.refresh = AsyncMock(side_effect=refresh_side_effect)
    result = await AutorService.create_autor(autor_data, db)
    db.add.assert_called()
    db.commit.assert_awaited()
    db.refresh.assert_awaited()

@pytest.mark.asyncio
async def test_actualizar_autor_not_found():
    db = AsyncMock()
    db.execute.return_value.scalar_one_or_none.return_value = None
    with pytest.raises(Exception):
        await AutorService.actualizar_autor(1, AutorUpdate(nombre="Nuevo"), db)

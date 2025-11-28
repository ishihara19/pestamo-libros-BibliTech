import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.tipo_documento_service import TipoDocumentoService
from app.schemas.tipo_documento_sch import TipoDocumentoCreate, TipoDocumentoUpdate

@pytest.mark.asyncio
async def test_create_tipo_documento():
    db = AsyncMock()
    db.add = MagicMock()
    db.commit = AsyncMock()
    db.refresh = AsyncMock()
    tipo_data = TipoDocumentoCreate(nombre="DNI", acronimo="DNI", descripcion="Documento Nacional de Identidad")
    from datetime import datetime
    def add_side_effect(obj):
        obj.id = 1
        obj.creado_en = datetime.now()
    db.add.side_effect = add_side_effect
    async def refresh_side_effect(obj):
        obj.id = 1
        obj.creado_en = datetime.now()
    db.refresh.side_effect = refresh_side_effect
    result = await TipoDocumentoService.create_tipo_documento(tipo_data, db)
    db.add.assert_called()
    db.commit.assert_awaited()
    db.refresh.assert_awaited()

@pytest.mark.asyncio
async def test_actualizar_tipo_documento_not_found():
    db = AsyncMock()
    db.execute.return_value.scalar.return_value = None
    with pytest.raises(Exception):
        await TipoDocumentoService.actualizar_tipo_documento(1, TipoDocumentoUpdate(nombre="Nuevo"), db)

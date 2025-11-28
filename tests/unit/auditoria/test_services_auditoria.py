import pytest
from unittest.mock import AsyncMock
from app.services.auditoria_service import AuditoriaService
import pytest
pytestmark = pytest.mark.asyncio

@pytest.mark.asyncio
async def test_obtener_auditoria_por_id_not_found():
    db = AsyncMock()
    db.execute.return_value.scalar_one_or_none.return_value = None
    with pytest.raises(Exception):
        await AuditoriaService.obtener_auditoria_por_id(1, db)

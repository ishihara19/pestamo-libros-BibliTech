import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.libro_service import LibroService
from app.schemas.libro_sch import LibroCreate

@pytest.mark.asyncio
async def test_create_libro():
    
    db = AsyncMock()
    db.add = MagicMock()
    db.commit = AsyncMock()
    db.refresh = AsyncMock()
    db.execute = AsyncMock()
    from datetime import date
    libro_data = LibroCreate(
        titulo="Libro de Prueba",
        descripcion="Descripción de prueba",
        categoria_id=1,
        editorial="Editorial X",
        fecha_publicacion=date(2020, 1, 1),
        autores_ids=[1, 2]
    )
    db.refresh.return_value = None
    # Mock para db.execute(select(Autor).where(Autor.id.in_(autores_ids)))
    autor1 = MagicMock()
    autor1.id = 1
    autor1.nombre = "Gabriel"
    autor1.apellido = "García"
    autor1.nacionalidad = "Colombiana"
    autor1._sa_instance_state = MagicMock()

    autor2 = MagicMock()
    autor2.id = 2
    autor2.nombre = "Mario"
    autor2.apellido = "Vargas"
    autor2.nacionalidad = "Peruana"
    autor2._sa_instance_state = MagicMock()
    class FakeScalars:
        def all(self):
            return [autor1, autor2]
    class FakeResult:
        def scalars(self):
            return FakeScalars()
        def scalar_one(self):
            # Simula el objeto Libro esperado por LibroView.model_validate
            libro_mock = MagicMock()
            libro_mock.id = 1
            libro_mock.titulo = "Libro de Prueba"
            libro_mock.descripcion = "Descripción de prueba"
            libro_mock.categoria_id = 1
            libro_mock.editorial = "Editorial X"
            from datetime import date, datetime
            libro_mock.fecha_publicacion = date(2020, 1, 1)
            libro_mock.creado_en = datetime.now()
            libro_mock.actualizado_en = datetime.now()
            libro_mock.imagen_url = "http://example.com/img.jpg"
            libro_mock.autores = [autor1, autor2]
            libro_mock.ejemplares_count = 0
            libro_mock.ejemplares_disponibles = 0
            libro_mock.ejemplares_reservados = 0
            libro_mock.ejemplares_prestados = 0
            libro_mock.ejemplares_danados = 0
            return libro_mock
    db.execute.return_value = FakeResult()
    # Mockear los atributos requeridos por Pydantic
    from datetime import datetime
    def add_side_effect(obj):
        obj.id = 1
        obj.creado_en = datetime.now()
        obj.actualizado_en = datetime.now()
        obj.imagen_url = "http://example.com/img.jpg"
    db.add.side_effect = add_side_effect
    async def refresh_side_effect(obj):
        obj.id = 1
        obj.creado_en = datetime.now()
        obj.actualizado_en = datetime.now()
        obj.imagen_url = "http://example.com/img.jpg"
    db.refresh.side_effect = refresh_side_effect
    await LibroService.create_libro(libro_data, db, imagen_url="http://example.com/img.jpg")
    db.add.assert_called()
    db.commit.assert_awaited()
    db.refresh.assert_awaited()

@pytest.mark.asyncio
async def test_create_libro_mocked():
    db = AsyncMock()
    db.add = MagicMock()
    db.commit = AsyncMock()
    db.refresh = AsyncMock()
    from datetime import date
    libro_data = LibroCreate(
        titulo="Cien Años de Soledad",
        descripcion="Novela emblemática",
        categoria_id=1,
        editorial="Editorial Sudamericana",
        fecha_publicacion=date(1967, 5, 30),
        autores_ids=[1]
    )
    # Mock para db.execute(select(Autor).where(Autor.id.in_(autores_ids)))
    autor1 = MagicMock()
    autor1.id = 1
    autor1.nombre = "Gabriel"
    autor1.apellido = "García"
    autor1.nacionalidad = "Colombiana"
    autor1._sa_instance_state = MagicMock()
    class FakeScalars:
        def all(self):
            return [autor1]
    class FakeResult:
        def scalars(self):
            return FakeScalars()
        def scalar_one(self):
            libro_mock = MagicMock()
            libro_mock.id = 1
            libro_mock.titulo = "Cien Años de Soledad"
            libro_mock.descripcion = "Novela emblemática"
            libro_mock.categoria_id = 1
            libro_mock.editorial = "Editorial Sudamericana"
            from datetime import date, datetime
            libro_mock.fecha_publicacion = date(1967, 5, 30)
            libro_mock.creado_en = datetime.now()
            libro_mock.actualizado_en = datetime.now()
            libro_mock.imagen_url = "url.jpg"
            libro_mock.autores = [autor1]
            libro_mock.ejemplares_count = 0
            libro_mock.ejemplares_disponibles = 0
            libro_mock.ejemplares_reservados = 0
            libro_mock.ejemplares_prestados = 0
            libro_mock.ejemplares_danados = 0
            return libro_mock
    db.execute.return_value = FakeResult()
    result = await LibroService.create_libro(libro_data, db, imagen_url="url.jpg")
    db.add.assert_called()
    db.commit.assert_awaited()
    db.refresh.assert_awaited()

from app.schemas.libro_sch import LibroBase, LibroCreate
from datetime import date

def test_libro_base_valid():
    libro = LibroBase(
        titulo="Libro de Prueba",
        descripcion="Descripción de prueba",
        categoria_id=1,
        editorial="Editorial X",
        fecha_publicacion=date(2020, 1, 1)
    )
    assert libro.titulo == "Libro de Prueba"
    assert libro.categoria_id == 1

def test_libro_create_with_autores():
    libro = LibroCreate(
        titulo="Libro de Prueba",
        descripcion="Descripción de prueba",
        categoria_id=1,
        editorial="Editorial X",
        fecha_publicacion=date(2020, 1, 1),
        autores_ids=[1, 2, 3]
    )
    assert libro.autores_ids == [1, 2, 3]

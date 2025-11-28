from app.schemas.ejemplar_sch import EjemplarBase, EjemplarCreate, EjemplarUpdate, EjemplarView, EjemplarReaderNormalized, EjemplarUpdateEstado
from datetime import date, datetime

def test_ejemplar_base():
    ej = EjemplarBase(libro_id=1, fecha_adquisicion=date(2020,1,1))
    assert ej.libro_id == 1

def test_ejemplar_create_inherits_base():
    ej = EjemplarCreate(libro_id=1, fecha_adquisicion=date(2020,1,1))
    assert isinstance(ej, EjemplarBase)

def test_ejemplar_update_partial():
    ej = EjemplarUpdate(libro_id=2)
    assert ej.libro_id == 2

def test_ejemplar_view_fields():
    now = datetime.now()
    ej = EjemplarView(id=1, libro_id=1, estado_id=1, fecha_adquisicion=date(2020,1,1), creado_en=now, actualizado_en=now, codigo_interno="A1")
    assert ej.id == 1

def test_ejemplar_reader_normalized():
    now = datetime.now()
    ej = EjemplarReaderNormalized(id=1, codigo_interno="A1", libro_titulo="El Quijote", estado_nombre="Disponible", fecha_adquisicion=date(2020,1,1), creado_en=now, actualizado_en=now)
    assert ej.libro_titulo == "El Quijote"

def test_ejemplar_update_estado():
    upd = EjemplarUpdateEstado(estado_id=2)
    assert upd.estado_id == 2

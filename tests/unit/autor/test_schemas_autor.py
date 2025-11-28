from app.schemas.autor_sch import AutorBase, AutorCreate, AutorUpdate, AutorView, AutorSimpleView
from datetime import date, datetime

def test_autor_base_valid():
    autor = AutorBase(nombre="Gabriel", apellido="García", fecha_nacimiento=date(1927,3,6), nacionalidad="Colombiana")
    assert autor.nombre == "Gabriel"
    assert autor.apellido == "García"
    assert autor.nacionalidad == "Colombiana"

def test_autor_create_inherits_base():
    autor = AutorCreate(nombre="Gabriel", apellido="García", fecha_nacimiento=date(1927,3,6), nacionalidad="Colombiana")
    assert isinstance(autor, AutorBase)

def test_autor_update_partial():
    autor = AutorUpdate(nombre="Gabo", fecha_nacimiento=None)
    assert autor.nombre == "Gabo"

def test_autor_view_fields():
    now = datetime.now()
    autor = AutorView(id=1, nombre="Gabriel", apellido="García", fecha_nacimiento=date(1927,3,6), nacionalidad="Colombiana", creado_en=now, actualizado_en=now)
    assert autor.id == 1

def test_autor_simple_view():
    autor = AutorSimpleView(id=1, nombre="Gabriel", apellido="García", nacionalidad="Colombiana")
    assert autor.nombre == "Gabriel"

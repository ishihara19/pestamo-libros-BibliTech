from app.schemas.categoria_sch import CategoriaBase, CategoriaCreate, CategoriaUpdate, CategoriaView
from datetime import datetime

def test_categoria_base():
    cat = CategoriaBase(nombre="Novela", descripcion="Narrativa literaria")
    assert cat.nombre == "Novela"

def test_categoria_create_inherits_base():
    cat = CategoriaCreate(nombre="Novela", descripcion="Narrativa literaria")
    assert isinstance(cat, CategoriaBase)

def test_categoria_update_partial():
    cat = CategoriaUpdate(nombre="Cuento")
    assert cat.nombre == "Cuento"

def test_categoria_view_fields():
    now = datetime.now()
    cat = CategoriaView(id=1, nombre="Novela", descripcion="Narrativa literaria", creado_en=now, actualizado_en=now)
    assert cat.id == 1

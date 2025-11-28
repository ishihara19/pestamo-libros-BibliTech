from app.schemas.estado_sch import EstadoBase, EstadoCreate, EstadoUpdate, EstadoView
from datetime import datetime

def test_estado_base():
    estado = EstadoBase(nombre="Activo", descripcion="En uso", tipo="general")
    assert estado.nombre == "Activo"

def test_estado_create_inherits_base():
    estado = EstadoCreate(nombre="Activo", descripcion="En uso", tipo="general")
    assert isinstance(estado, EstadoBase)

def test_estado_update_partial():
    estado = EstadoUpdate(nombre="Inactivo")
    assert estado.nombre == "Inactivo"

def test_estado_view_fields():
    now = datetime.now()
    estado = EstadoView(id=1, nombre="Activo", descripcion="En uso", tipo="general", creado_en=now, actualizado_en=now)
    assert estado.id == 1

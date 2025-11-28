from app.schemas.rol_sch import RolBase, RolCreate, RolUpdate, RolView
from datetime import datetime

def test_rol_base_validation():
    rol = RolBase(nombre="Admin", acronimo="ADM", descripcion="Administrador")
    assert rol.nombre == "Admin"
    assert rol.acronimo == "ADM"

def test_rol_update_partial():
    rol = RolUpdate(nombre="Nuevo")
    assert rol.nombre == "Nuevo"
    assert rol.acronimo is None

def test_rol_view_model_validate():
    now = datetime.now()
    data = {"id": 1, "nombre": "Admin", "acronimo": "ADM", "descripcion": "desc", "creado_en": now, "actualizado_en": now}
    rol = RolView.model_validate(data)
    assert rol.id == 1
    assert rol.nombre == "Admin"

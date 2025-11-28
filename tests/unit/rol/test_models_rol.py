from app.models.rol import Rol

def test_rol_model_fields():
    rol = Rol(nombre="Admin", acronimo="ADM", descripcion="desc")
    assert rol.nombre == "Admin"
    assert rol.acronimo == "ADM"
    assert rol.descripcion == "desc"

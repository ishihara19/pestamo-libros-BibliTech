from app.models.estado import Estado

def test_estado_model_fields():
    estado = Estado(nombre="Activo", descripcion="En uso", tipo="general")
    assert estado.nombre == "Activo"
    assert estado.tipo == "general"

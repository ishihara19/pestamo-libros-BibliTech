from app.models.tipo_documento import TipoDocumento

def test_tipo_documento_model_fields():
    tipo = TipoDocumento(nombre="DNI", acronimo="DNI", descripcion="Documento Nacional de Identidad")
    assert tipo.nombre == "DNI"
    assert tipo.acronimo == "DNI"
    assert tipo.descripcion == "Documento Nacional de Identidad"

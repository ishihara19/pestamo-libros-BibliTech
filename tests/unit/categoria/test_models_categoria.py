from app.models.categoria import Categoria

def test_categoria_model_fields():
    cat = Categoria(nombre="Novela", descripcion="Narrativa literaria")
    assert cat.nombre == "Novela"
    assert cat.descripcion == "Narrativa literaria"

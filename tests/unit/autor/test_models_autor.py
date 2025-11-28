from app.models.autor import Autor

def test_autor_model_fields():
    autor = Autor(
        nombre="Gabriel",
        apellido="García",
        fecha_nacimiento=None,
        nacionalidad="Colombiana"
    )
    assert autor.nombre == "Gabriel"
    assert autor.apellido == "García"
    assert autor.nacionalidad == "Colombiana"

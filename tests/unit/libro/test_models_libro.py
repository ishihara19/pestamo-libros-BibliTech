from app.models.libro import Libro

def test_libro_model_fields():
    libro = Libro(
        titulo="Libro de Prueba",
        descripcion="Descripción de prueba",
        categoria_id=1,
        editorial="Editorial X",
        fecha_publicacion=None,
        imagen_url="http://example.com/img.jpg"
    )
    assert libro.titulo == "Libro de Prueba"
    assert libro.categoria_id == 1
    assert libro.imagen_url == "http://example.com/img.jpg"

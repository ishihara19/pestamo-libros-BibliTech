from app.models.autor_libro import autor_libro

def test_autor_libro_table_columns():
    columns = [c.name for c in autor_libro.columns]
    assert "autor_id" in columns
    assert "libro_id" in columns

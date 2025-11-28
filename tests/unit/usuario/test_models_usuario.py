from app.models.usuario import Usuario

def test_usuario_model_fields():
    usuario = Usuario(
        correo="test@example.com",
        nombre="Juan",
        apellido="Pérez",
        documento="123456",
        contrasena="Abcdef1!",
        tipo_documento_id=1,
        estado_id=1,
        rol_id=1,
        telefono="3001234567",
        direccion="Calle 1",
        fecha_nacimiento=None
    )
    assert usuario.nombre == "Juan"
    assert usuario.apellido == "Pérez"
    assert usuario.correo == "test@example.com"

from app.utils.utils import normalizar_correo, validar_complejidad_contrasena, normalizar_nombre_propio
import pytest

def test_normalizar_correo():
    assert normalizar_correo("  TEST@EXAMPLE.com ") == "test@example.com"
    assert normalizar_correo("") == ""

def test_validar_complejidad_contrasena_valida():
    assert validar_complejidad_contrasena("Abcdef1!") == "Abcdef1!"

def test_validar_complejidad_contrasena_invalida():
    with pytest.raises(ValueError):
        validar_complejidad_contrasena("abcdef1!")  # Falta mayúscula
    with pytest.raises(ValueError):
        validar_complejidad_contrasena("ABCDEF1!")  # Falta minúscula
    with pytest.raises(ValueError):
        validar_complejidad_contrasena("Abcdefgh!") # Falta número

def test_normalizar_nombre_propio():
    assert normalizar_nombre_propio("juan perez") == "Juan Perez"
    assert normalizar_nombre_propio("  maria de la cruz  ") == "Maria de la Cruz"

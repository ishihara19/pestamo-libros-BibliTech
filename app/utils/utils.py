import re
def normalizar_correo(correo: str) -> str:
    """
    Normaliza una dirección de correo electrónico.
    
    - Elimina espacios en blanco al inicio y al final.
    - Convierte todo a minúsculas.
    """
    if not correo:
        return correo
    return correo.strip().lower()

def validar_complejidad_contrasena(v: str) -> str:
    """Valida la complejidad de la contraseña."""
    if not re.search(r"[a-z]", v):
        raise ValueError("La contraseña debe contener al menos una letra minúscula")
    if not re.search(r"[A-Z]", v):
        raise ValueError("La contraseña debe contener al menos una letra mayúscula")
    if not re.search(r"[0-9]", v):
        raise ValueError("La contraseña debe contener al menos un número")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
        raise ValueError("La contraseña debe contener al menos un carácter especial")
    return v  
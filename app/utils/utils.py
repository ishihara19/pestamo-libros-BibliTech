
def normalizar_correo(correo: str) -> str:
    """
    Normaliza una dirección de correo electrónico.
    
    - Elimina espacios en blanco al inicio y al final.
    - Convierte todo a minúsculas.
    """
    if not correo:
        return correo
    return correo.strip().lower()
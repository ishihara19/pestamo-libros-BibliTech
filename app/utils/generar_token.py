import string
import secrets

def generar_token(size: int = 12) -> str:
    """
    Genera un token alfanumérico seguro de longitud especificada (por defecto 12).
    Usa el módulo 'secrets' para asegurar aleatoriedad criptográfica.
    """
    caracteres = string.ascii_letters + string.digits  # A-Z, a-z, 0-9
    return ''.join(secrets.choice(caracteres) for _ in range(size))
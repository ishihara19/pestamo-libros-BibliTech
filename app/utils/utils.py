import re
from datetime import date
from ..core.config import settings


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
    if not re.search(r"[!@#$%^&*.,-:()_]", v):
        raise ValueError(
            "La contraseña debe contener al menos un carácter especial de !@#$%^&*.,-:()_"
        )
    return v


def normalizar_nombre_propio(texto: str) -> str:
    """
    Normaliza un nombre propio:
    - Capitaliza la primera letra de cada palabra.
    - Mantiene minúsculas en preposiciones y artículos comunes (de, del, la, etc.).
    - Limpia espacios extra.
    """
    if not texto:
        return texto

    texto = " ".join(texto.split())  # elimina espacios dobles

    excepciones = {
        "de",
        "del",
        "la",
        "las",
        "los",
        "y",
        "e",
        "da",
        "das",
        "do",
        "dos",
        "van",
        "von",
    }

    palabras = texto.split()
    resultado = []

    for i, palabra in enumerate(palabras):
        palabra_lower = palabra.lower()

        # La primera palabra siempre se capitaliza
        if i == 0 or palabra_lower not in excepciones:
            palabra_normalizada = palabra_lower.capitalize()
        else:
            palabra_normalizada = palabra_lower

        resultado.append(palabra_normalizada)

    return " ".join(resultado)


def calcular_edad(fecha_nacimiento: date) -> int:
    """Devuelve la edad en años a partir de fecha_nacimiento."""
    hoy = date.today()
    return (
        hoy.year
        - fecha_nacimiento.year
        - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
    )


def tiene_edad_minima(fecha_nacimiento: date, edad_minima: int) -> bool:
    """Verifica si la fecha de nacimiento indica que la persona tiene al menos la edad mínima."""
    if not fecha_nacimiento:
        return False
    return calcular_edad(fecha_nacimiento) >= edad_minima


def validar_tipo_documento_edad(tipo_documento: str, fecha_nacimiento: date) -> bool:
    """
    Valida que el tipo de documento sea coherente con la edad del usuario.

    - "C.C" para mayores de 18 años.
    - "T.I" para menores de 18 años.
    """
    if not tipo_documento or not fecha_nacimiento:
        return True  # si falta alguno, no valida aún

    edad = calcular_edad(fecha_nacimiento)
    tipo_documento = str(tipo_documento).upper().strip()

    if tipo_documento == settings.DOCUMENTO_MAYOR_EDAD_ID and edad < 18:
        raise ValueError("El tipo de documento 'C.C' es solo para mayores de 18 años.")
    if tipo_documento == settings.DOCUMENTO_MENOR_EDAD_ID and edad >= 18:
        raise ValueError("El tipo de documento 'T.I' es solo para menores de 18 años.")
    return True

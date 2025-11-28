import re
from datetime import date, timedelta
import magic
from PIL import Image
import io
from ..core.config import settings

ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp"}


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

async def validate_max_size_image(file_bytes: bytes, max_size_mb: int = 2) -> None:
    """
    Valida que el tamaño del archivo no exceda el máximo permitido.
        file_bytes: Bytes del archivo a validar.
        max_size_mb: Tamaño máximo permitido en megabytes.
    """
    size_mb = len(file_bytes) / (1024 * 1024)
    if size_mb > max_size_mb:
        raise ValueError(f"El tamaño del archivo excede el máximo permitido de {max_size_mb} MB.")
    
async def validate_image(file_bytes: bytes) -> str:
    """
    Valida que el archivo sea realmente una imagen permitida.
    Retorna el tipo MIME si es válido.
        file_bytes: Bytes del archivo a validar.
        mime_type: Tipo MIME del archivo.
    """
        
    mime_type = magic.from_buffer(file_bytes, mime=True)
    if mime_type not in ALLOWED_MIME_TYPES:
        raise ValueError(f"Tipo de archivo no permitido: {mime_type}")
    return mime_type

async def convert_to_webp(file_bytes: bytes, quality: int = 80) -> bytes:
    """
    Convierte cualquier imagen a formato WebP optimizado.
    Retorna los bytes de la imagen en formato WebP.
        image: Bytes de la imagen original.
        quality: Calidad de compresión WebP (1-100).
    """
    image = Image.open(io.BytesIO(file_bytes)).convert("RGB")
    output = io.BytesIO()
    image.save(output, format="WEBP", optimize=True, quality=quality)
    return output.getvalue()


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from ..models.ejemplar import Ejemplar  # importa tu modelo real

async def generar_codigo_unico(libro_id: int, session: AsyncSession) -> str:
    """
    Genera un código interno único para un ejemplar de un libro usando SQLAlchemy async.
    Formato: L####-E###
    """
    # Buscar el código más alto actual para ese libro
    stmt = (
        select(Ejemplar.codigo_interno)
        .where(Ejemplar.libro_id == libro_id)
        .order_by(Ejemplar.codigo_interno.desc())
        .limit(1)
    )

    result = await session.execute(stmt)
    row = result.scalar_one_or_none()

    # Si no hay ejemplares aún
    if not row:
        return f"L{libro_id:04d}-E001"

    # Extraer el número del ejemplar más alto
    num_actual = int(row.split("-E")[-1])
    siguiente = num_actual + 1

    # Generar el nuevo código
    return f"L{libro_id:04d}-E{siguiente:03d}"

async def generar_fecha_devolucion_prevista(
    fecha_solicitud: date, dias_prestamo: int = 14
) -> date:
    """
    Genera la fecha prevista de devolución sumando días calendario a la fecha de solicitud.
    Valida que la cantidad de días no sea menor a 1 y permite fines de semana.
    """

    # Validación: el número de días no puede ser menor que 1
    if dias_prestamo < 1:
        raise ValueError("El número de días de préstamo no puede ser menor a 1.")

    
    fecha_devolucion = fecha_solicitud + timedelta(days=dias_prestamo)

    return fecha_devolucion

async def ejemplar_disponible(ejemplar_id: int, session: AsyncSession) -> bool:
    """
    Verifica si un ejemplar está disponible para préstamo.
    Retorna True si está disponible, False si está prestado.
    """
    stmt = select(Ejemplar).where(Ejemplar.id == ejemplar_id)
    result = await session.execute(stmt)
    ejemplar = result.scalar_one_or_none()

    if not ejemplar:
        raise ValueError("El ejemplar no existe.")

    return ejemplar.estado_id == 1

async def ejemplar_disponible_info(libro_id: int, session: AsyncSession) -> dict | None:
    """
    Retorna:
    - id del ejemplar
    - codigo_interno del ejemplar
    Si no hay ejemplares disponibles, retorna None.
    """
    stmt = (
        select(Ejemplar.id, Ejemplar.codigo_interno)
        .where(Ejemplar.libro_id == libro_id)
        .where(Ejemplar.estado_id == settings.DISPONIBILIDAD_EJEMPLAR_DISPONIBLE_ID)
        .limit(1)
    )

    result = await session.execute(stmt)
    row = result.one_or_none()    

    if not row:
        return None

    return {
        "id": row.id,
        "codigo_interno": row.codigo_interno,
    }


async def total_ejemplares_disponibles_por_libro(libro_id: int, session: AsyncSession) -> int:
    """
    Retorna la cantidad total de ejemplares disponibles (estado_id = 1)
    para un libro dado.
    """
    stmt = (
        select(func.count(Ejemplar.id))
        .where(Ejemplar.libro_id == libro_id)
        .where(Ejemplar.estado_id == settings.DISPONIBILIDAD_EJEMPLAR_DISPONIBLE_ID)
    )

    result = await session.execute(stmt)
    return result.scalar() or 0


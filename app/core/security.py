from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import timedelta
from sqlalchemy import select
from fastapi import Request
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.usuario import Usuario
from ..core.db.postgre import get_session
from ..core.config import settings
from ..utils.tiempo_tz import get_time_now
from ..utils.utils import normalizar_correo

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash una contraseña usando bcrypt.
    Args:
        password (str): La contraseña a hashear.
    Returns:
        str: La contraseña hasheada.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica una contraseña en texto plano contra una contraseña hash.
    Args:
        plain_password (str): La contraseña en texto plano a verificar.
        hashed_password (str): La contraseña hash con la que comparar.
    Returns:
        bool: True si las contraseñas coinciden, False de lo contrario.
    """
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(email: str, password: str, db: AsyncSession):
    """
    Autentica a un usuario verificando su correo electrónico y contraseña.
    Args:
        email (str): El correo electrónico del usuario.
        password (str): La contraseña del usuario.
    Returns:
        str: El ID del usuario si la autenticación es exitosa, None en caso contrario.
    """
    email = normalizar_correo(email)
    result = await db.execute(select(Usuario).where(Usuario.correo == email))
    user = result.scalars().first()
    
    
    if not user or not verify_password(password, user.contrasena):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    return str(user.id)


def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Crea un JWT access token.
    Args:
        data (dict): Los datos a codificar en el token.
        expires_delta (timedelta, optional): El tiempo de expiración del token. Por defecto es None.
    Returns:
        str: El JWT access token codificado.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = get_time_now() + expires_delta
    else:
        expire = get_time_now() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta = None):
    """
    Crea un JWT refresh token.
    Args:
        data (dict): Los datos a codificar en el token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = get_time_now() + expires_delta
    else:
        expire = get_time_now() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encode_rfsh = jwt.encode(
        to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
    )
    return encode_rfsh
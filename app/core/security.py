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
    Hash a password using bcrypt.
    Args:
        password (str): The password to hash.
    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    Args:
        plain_password (str): The plain password to verify.
        hashed_password (str): The hashed password to compare against.
    Returns:
        bool: True if the passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(email: str, password: str, db: AsyncSession):
    """
    Authenticate a user by verifying their email and password.
    Args:
        email (str): The user's email.
        password (str): The user's password.
    Returns:
        str: The user's ID if authentication is successful, None otherwise.
    """
    
    email = normalizar_correo(email)
    async with db as session:
        result = await session.execute(
            select(Usuario).where(Usuario.correo == email)
        )
        user = result.scalars().first()

    if not user or not verify_password(password, user.contrasena):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return str(user.id)


def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Create a JWT access token.
    Args:
        data (dict): The data to encode in the token.
        expires_delta (timedelta, optional): The expiration time for the token. Defaults to None.
    Returns:
        str: The encoded JWT access token.
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
    Create a JWT refresh token.
    Args:
        data (dict): The data to encode in the token.
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
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status,Request
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from ..core.db.postgre import get_session
from ..models.usuario import Usuario
from ..core.config import settings
from ..schemas.usuario_sch import UsuarioView, UsuarioReadNormalized

oauth2_schema = OAuth2PasswordBearer(tokenUrl=f"{settings.PREFIX_API_VERSION}/auth/inicio-sesion")


async def obtener_usuario_actual(
    request: Request,
    token: str = Depends(oauth2_schema),
    db: AsyncSession = Depends(get_session)
) -> Usuario:
    """
    Obtener el usuario actual del token JWT + IP y Host.
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        usuario_id = int(payload.get("sub"))
        if usuario_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

        # Cargar usuario
        result = await db.execute(
            select(Usuario)
            .options(
                selectinload(Usuario.rol),
                selectinload(Usuario.estado),
                selectinload(Usuario.tipo_documento),
            )
            .where(Usuario.id == usuario_id)
        )
        usuario = result.scalars().first()
        if not usuario:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado")

        # Capturar IP y host del request
        ip = request.headers.get("x-forwarded-for", request.client.host).split(",")[0]
        host = request.headers.get("host", "sistema")        

       
        usuario.ip = ip
        usuario.host = host
        usuario.username = usuario.correo

        return usuario

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    
async def obtener_usuario_actual_activo(
    usuario_actual: Annotated[Usuario, Depends(obtener_usuario_actual),]
):
    if usuario_actual.estado_id != settings.ESTADO_ACTIVO:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail= "Usuario inactivo"
        )
    return usuario_actual


async def obtener_usuario_actual_administrador(
    usuario_actual: Annotated[Usuario, Depends(obtener_usuario_actual_activo),]
):
    if usuario_actual.rol_id != settings.ROL_ADMIN:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail= "Sin autorización"
        )
    return UsuarioReadNormalized.from_model(usuario_actual)
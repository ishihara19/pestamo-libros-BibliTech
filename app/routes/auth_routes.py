from fastapi import APIRouter, HTTPException, Depends, status, Request
from typing import Annotated
from datetime import datetime
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordRequestForm
from ..core.security import (
     hash_password,
    create_access_token,
    create_refresh_token,
    authenticate_user,
)
from ..core.db.postgre import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.jwt_sch import Token, TokenRefreshRequest, RefreshTokenResponse, TokenData
from ..core.config import settings
from ..schemas.usuario_sch import UsuarioReadNormalized, UsuarioCreate,UsuarioView
from ..services.usuario_service import UsuarioService
from ..dependencies.auth import obterner_usuario_actual_activo
from ..models.usuario   import  Usuario


auth = APIRouter(prefix="/auth", tags=["auth"])

@auth.post("/registro", response_model=UsuarioView, status_code=201)
async def registrar_usuario(
    usuario: UsuarioCreate,
    db: AsyncSession = Depends(get_session)
):
    
    """Crear un nuevo usuario"""
    return await UsuarioService.create_usuario(usuario, db)

@auth.post("/inicio-sesion", response_model=Token)
async def iniciar_sesion(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_session)
) -> Token:
    """Iniciar sesión de usuario"""
    usuario = await authenticate_user(form_data.username, form_data.password, db)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token = create_access_token(data={"sub": usuario})
    refresh_token = create_refresh_token(data={"sub": usuario})
    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")

@auth.get("/yo", response_model=UsuarioReadNormalized)
async def obtener_yo(
    usuario_actual: Usuario = Depends(obterner_usuario_actual_activo)
):
    return UsuarioReadNormalized.from_model(usuario_actual)
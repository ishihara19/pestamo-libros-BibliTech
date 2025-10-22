from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from ..core.db.postgre import get_session
from ..schemas.paginacion_sch import PaginationParams, PaginatedResponse
from ..schemas.usuario_sch import (
    UsuarioCreate,
    UsuarioView,
    UsuarioUpdatePerfil,
    UsuarioUpdateContrasena,
    UsuarioResetearContrasena,
    UsuarioVerificarToken,
    UsuarioMensaje
)
from ..services.usuario_service import UsuarioService

usuario_router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@usuario_router.post("", response_model=UsuarioView, status_code=201)
async def crear_usuario(
    usuario: UsuarioCreate,
    db: AsyncSession = Depends(get_session)
):
    """Crear un nuevo usuario"""
    return await UsuarioService.create_usuario(usuario, db)

@usuario_router.get("", response_model=list[UsuarioView] | PaginatedResponse[UsuarioView])
async def listar_usuarios(
    db: AsyncSession = Depends(get_session),
    page: int | None = Query(None, ge=1, description="Número de página"),
    page_size: int | None = Query(None, ge=1, le=100, description="Items por página")
):
    """
    Listar todos los usuarios.
    Usa paginación si se proveen los parámetros page y page_size.
    """
    pagination = None
    if page is not None and page_size is not None:
        pagination = PaginationParams(page=page, page_size=page_size)
    
    return await UsuarioService.listar_usuarios(db, pagination)

@usuario_router.get("/{id}", response_model=UsuarioView)
async def obtener_usuario(
    id: int,
    db: AsyncSession = Depends(get_session)
):
    """Obtener un usuario por su ID"""
    usuario = await UsuarioService.obtener_usuario(id, db)
    if not usuario:       
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@usuario_router.put("/{id}/perfil", response_model=UsuarioView)
async def actualizar_perfil_usuario(
    id: int,
    usuario_update: UsuarioUpdatePerfil,
    db: AsyncSession = Depends(get_session)
):
    """Actualizar el perfil de un usuario existente"""
    return await UsuarioService.actualizar_perfil_usuario(id, usuario_update, db)

@usuario_router.put("/{id}/contrasena", response_model=UsuarioMensaje)
async def actualizar_contrasena_usuario(
    id: int,
    contrasena_update: UsuarioUpdateContrasena,
    db: AsyncSession = Depends(get_session)
):
    """Actualizar la contraseña de un usuario existente"""
    return await UsuarioService.actualizar_contrasena_usuario(id, contrasena_update, db)

@usuario_router.post("/resetear-contrasena", response_model=UsuarioMensaje)
async def restablecer_contrasena_usuario(
    contrasena_resetear: UsuarioResetearContrasena,
    db: AsyncSession = Depends(get_session)
):
    """Restablecer la contraseña de un usuario"""
    return await UsuarioService.restablecer_contrasena_usuario(contrasena_resetear, db)

@usuario_router.post("/verificar-token", response_model=UsuarioMensaje)
async def verificar_token_usuario(
    verificacion: UsuarioVerificarToken,
    db: AsyncSession = Depends(get_session)
):
    """Verificar el token y restablecer la contraseña"""
    return await UsuarioService.verificar_token_usuario(verificacion, db)

@usuario_router.delete("/{id}", status_code=204)
async def eliminar_usuario(
    id: int,
    db: AsyncSession = Depends(get_session)
):
    """Eliminar un usuario existente"""
    await UsuarioService.eliminar_usuario(id, db)
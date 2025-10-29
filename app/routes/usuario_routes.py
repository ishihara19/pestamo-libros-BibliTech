from fastapi import APIRouter, Depends, Query, Request
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
    UsuarioMensaje,
    UsuarioReadNormalized,
)
from ..services.usuario_service import UsuarioService
from ..dependencies.auth import (
    obtener_usuario_actual_administrador,
    obtener_usuario_actual_activo,
)
from ..models.usuario import Usuario

usuario_router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@usuario_router.post("", response_model=UsuarioView, status_code=201)
async def crear_usuario(
    usuario: UsuarioCreate,
    db: AsyncSession = Depends(get_session),
    usuario_admin: Usuario = Depends(obtener_usuario_actual_administrador),
):
    """Crear un nuevo usuario"""
    ip = usuario_admin.ip
    host = usuario_admin.host
    username = usuario_admin.username

    return await UsuarioService.create_usuario(usuario, db, host, ip, username)


@usuario_router.get(
    "",
    response_model=list[UsuarioView]
    | PaginatedResponse[UsuarioView]
    | list[UsuarioReadNormalized]
    | PaginatedResponse[UsuarioReadNormalized],
)
async def listar_usuarios(
    normalizado: bool = Query(False, description="Retornar correos normalizados"),
    db: AsyncSession = Depends(get_session),
    page: int | None = Query(None, ge=1, description="Número de página"),
    page_size: int | None = Query(None, ge=1, le=100, description="Items por página"),
    usuario_admin: Usuario = Depends(obtener_usuario_actual_administrador),
):
    """
    Listar todos los usuarios.
    Usa paginación si se proveen los parámetros page y page_size.
    """
    pagination = None
    if page is not None and page_size is not None:
        pagination = PaginationParams(page=page, page_size=page_size)

    return await UsuarioService.listar_usuarios(db, pagination, normalizado)


@usuario_router.get("/{id}", response_model=UsuarioView | UsuarioReadNormalized | None)
async def obtener_usuario(
    id: int,
    db: AsyncSession = Depends(get_session),
    normalizado: bool = Query(False, description="Retornar correo normalizado"),
    usuario_actual: Usuario = Depends(obtener_usuario_actual_activo),
):
    """Obtener un usuario por su ID"""
    usuario = await UsuarioService.obtener_usuario(id, normalizado, db)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@usuario_router.put("/{id}/perfil", response_model=UsuarioReadNormalized)
async def actualizar_perfil_usuario(
    id: int,
    usuario_update: UsuarioUpdatePerfil,
    db: AsyncSession = Depends(get_session),
    usuario_actual: Usuario = Depends(obtener_usuario_actual_activo),
):
    """Actualizar el perfil de un usuario existente"""
    ip = usuario_actual.ip
    host = usuario_actual.host
    username = usuario_actual.username
    return await UsuarioService.actualizar_perfil_usuario(
        id, usuario_update, db, ip, host, username
    )


@usuario_router.put("/{id}/contrasena", response_model=UsuarioMensaje)
async def actualizar_contrasena_usuario(
    id: int,
    contrasena_update: UsuarioUpdateContrasena,
    db: AsyncSession = Depends(get_session),
    usuario_actual: Usuario = Depends(obtener_usuario_actual_activo),
):
    """Actualizar la contraseña de un usuario existente"""
    ip = usuario_actual.ip
    host = usuario_actual.host
    username = usuario_actual.username
    return await UsuarioService.actualizar_contrasena_usuario(
        id, contrasena_update, db, ip, host, username
    )


@usuario_router.post("/resetear-contrasena", response_model=UsuarioMensaje)
async def restablecer_contrasena_usuario(
    contrasena_resetear: UsuarioResetearContrasena,
    request: Request,
    db: AsyncSession = Depends(get_session),    
):
    """Restablecer la contraseña de un usuario"""
    ip = request.headers.get("x-forwarded-for", request.client.host).split(",")[0]
    host = request.headers.get("host")
    return await UsuarioService.restablecer_contrasena_usuario(
        contrasena_resetear, db, ip, host
    )


@usuario_router.post("/verificar-token", response_model=UsuarioMensaje)
async def verificar_token_usuario(
    verificacion: UsuarioVerificarToken,
    request: Request,
    db: AsyncSession = Depends(get_session),    
):
    """Verificar el token y restablecer la contraseña"""
    ip = request.headers.get("x-forwarded-for", request.client.host).split(",")[0]
    host = request.headers.get("host", "sistema")
    return await UsuarioService.verificar_token_usuario(verificacion, db, ip, host)


@usuario_router.delete("/{id}/suave", response_model=UsuarioMensaje)
async def eliminar_usuario_suave(
    id: int,
    db: AsyncSession = Depends(get_session),
    usuario_admin: Usuario = Depends(obtener_usuario_actual_administrador),
):
    """Eliminar un usuario existente de forma suave (soft delete)"""
    ip = usuario_admin.ip
    host = usuario_admin.host
    username = usuario_admin.username
    return await UsuarioService.eliminar_usuario_suave(id, db, ip, host, username)


@usuario_router.delete("/{id}", status_code=204)
async def eliminar_usuario(
    id: int,
    db: AsyncSession = Depends(get_session),
    usuario_admin: Usuario = Depends(obtener_usuario_actual_administrador),
):
    """Eliminar un usuario existente"""
    ip = usuario_admin.ip
    host = usuario_admin.host
    username = usuario_admin.username
    return await UsuarioService.eliminar_usuario(id, db, ip, host, username)

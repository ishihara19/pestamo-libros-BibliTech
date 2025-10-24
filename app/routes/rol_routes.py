from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from ..core.db.postgre import get_session
from ..schemas.paginacion_sch import PaginationParams, PaginatedResponse
from ..schemas.rol_sch import RolCreate, RolView, RolUpdate
from ..services.rol_service import RolService
from ..dependencies.auth import obterner_usuario_actual_superusuario, obterner_usuario_actual_activo
from ..models.usuario import Usuario

rol_router = APIRouter(prefix="/roles", tags=["Roles"])

@rol_router.post("", response_model=RolView, status_code=201)
async def crear_rol(
    rol: RolCreate,
    db: AsyncSession = Depends(get_session),
    usuario_admin: Usuario = Depends(obterner_usuario_actual_superusuario)
):
    """Crear un nuevo rol"""
    return await RolService.create_role(rol, db)

@rol_router.get("", response_model=list[RolView] | PaginatedResponse[RolView])
async def listar_roles(
    db: AsyncSession = Depends(get_session),
    page: int | None = Query(None, ge=1, description="Número de página"),
    page_size: int | None = Query(None, ge=1, le=100, description="Items por página")
):
    """
    Listar todos los roles.
    Usa paginación si se proveen los parámetros page y page_size.
    """
    pagination = None
    if page is not None and page_size is not None:
        pagination = PaginationParams(page=page, page_size=page_size)
    
    return await RolService.listar_roles(db, pagination)

@rol_router.get("/{id}", response_model=RolView)
async def obtener_rol(
    id: int,
    db: AsyncSession = Depends(get_session),
    usuario_actual: Usuario = Depends(obterner_usuario_actual_activo)
):
    """Obtener un rol por su ID"""
    rol = await RolService.obtener_role(id, db)
    if not rol:       
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return rol

@rol_router.put("/{id}", response_model=RolView)
async def actualizar_rol(
    id: int,
    rol_update: RolUpdate,
    db: AsyncSession = Depends(get_session),
    usuario_admin: Usuario = Depends(obterner_usuario_actual_superusuario)
):
    """Actualizar un rol existente"""
    return await RolService.actualizar_role(id, rol_update, db)

@rol_router.delete("/{id}", status_code=204)
async def eliminar_rol(
    id: int,
    db: AsyncSession = Depends(get_session),
    usuario_admin: Usuario = Depends(obterner_usuario_actual_superusuario)
):
    """Eliminar un rol existente"""
    await RolService.eliminar_role(id, db)
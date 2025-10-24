from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.estado_sch import EstadoCreate, EstadoUpdate, EstadoView
from ..schemas.paginacion_sch import PaginationParams, PaginatedResponse
from ..services.estado_service import EstadoService
from ..core.db.postgre import get_session
from ..dependencies.auth import obterner_usuario_actual_superusuario, obterner_usuario_actual_activo
from ..models.usuario import Usuario

estado_router = APIRouter(prefix="/estados", tags=["Estados"])


@estado_router.post("", response_model=EstadoView, status_code=201)
async def crear_estado(
    estado: EstadoCreate,
    db: AsyncSession = Depends(get_session),
    usuario_admin: Usuario = Depends(obterner_usuario_actual_superusuario)
):
    """Crear un nuevo estado"""
    return await EstadoService.create_estado(estado, db)

@estado_router.get("", response_model=list[EstadoView] | PaginatedResponse[EstadoView])
async def listar_estados(
    db: AsyncSession = Depends(get_session),
    page: int | None = Query(None, ge=1, description="Número de página"),
    page_size: int | None = Query(None, ge=1, le=100, description="Items por página")
):
    """
    Listar todos los estados.
    Usa paginación si se proveen los parámetros page y page_size.
    """
    pagination = None
    if page is not None and page_size is not None:
        pagination = PaginationParams(page=page, page_size=page_size)
    
    return await EstadoService.listar_estados(db, pagination)

@estado_router.get("/tipo", response_model=list[EstadoView] | PaginatedResponse[EstadoView])
async def listar_estados_por_tipo(
    db: AsyncSession = Depends(get_session),
    type: str = Query(description=(
            "Tipo de estado. Ejemplos válidos:\n"
            "- usuario\n"
            "- libro\n"
            "- prestamo"
        ), default="usuario"),
    page: int | None = Query(None, ge=1, description="Número de página"),
    page_size: int | None = Query(None, ge=1, le=100, description="Items por página")
):
    """Listar estados de tipo específico
    Usa paginación si se proveen los parámetros page y page_size.
    """
    pagination = None
    if page is not None and page_size is not None:
        pagination = PaginationParams(page=page, page_size=page_size)
    
    return await EstadoService.listar_estado_por_tipo(db, type, pagination)

@estado_router.get("/{id}", response_model=EstadoView)
async def obtener_estado(
    id: int,
    db: AsyncSession = Depends(get_session),
    usuario_actual: Usuario = Depends(obterner_usuario_actual_activo)
):
    """Obtener un estado por ID"""
    return await EstadoService.obtener_estado_id(id, db)


@estado_router.put("/{id}", response_model=EstadoView)
async def actualizar_estado(
    id: int,
    estado_update: EstadoUpdate,
    db: AsyncSession = Depends(get_session),
    usuario_admin: Usuario = Depends(obterner_usuario_actual_superusuario)
):
    """Actualizar un estado existente"""
    return await EstadoService.actualizar_estado(id, estado_update, db)


@estado_router.delete("/{id}", status_code=204)
async def eliminar_estado(
    id: int,
    db: AsyncSession = Depends(get_session),
    usuario_admin: Usuario = Depends(obterner_usuario_actual_superusuario)
):
    """Eliminar un estado"""
    await EstadoService.eliminar_estado(id, db)
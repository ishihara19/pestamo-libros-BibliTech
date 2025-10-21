from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.estado_sch import EstadoCreate, EstadoUpdate, EstadoView
from ..schemas.paginacion_sch import PaginationParams, PaginatedResponse
from ..services.estado_service import EstadoService
from ..core.db.postgre import get_session

estado_router = APIRouter(prefix="/estados", tags=["Estados"])


@estado_router.post("", response_model=EstadoView, status_code=201)
async def crear_estado(
    estado: EstadoCreate,
    db: AsyncSession = Depends(get_session)
):
    """Crear un nuevo estado"""
    return await EstadoService.create_estado(estado, db)

""""""
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


@estado_router.get("/usuario", response_model=list[EstadoView] | PaginatedResponse[EstadoView])
async def listar_estados_usuario(
    db: AsyncSession = Depends(get_session),
    page: int | None = Query(None, ge=1),
    page_size: int | None = Query(None, ge=1, le=100)
):
    """Listar estados de tipo usuario
    Usa paginación si se proveen los parámetros page y page_size.
    """
    pagination = None
    if page is not None and page_size is not None:
        pagination = PaginationParams(page=page, page_size=page_size)
    
    return await EstadoService.listar_estado_usuario(db, pagination)


@estado_router.get("/libro", response_model=list[EstadoView] | PaginatedResponse[EstadoView])
async def listar_estados_libro(
    db: AsyncSession = Depends(get_session),
    page: int | None = Query(None, ge=1),
    page_size: int | None = Query(None, ge=1, le=100)
):
    """Listar estados de tipo libro
    Usa paginación si se proveen los parámetros page y page_size.
    """
    pagination = None
    if page is not None and page_size is not None:
        pagination = PaginationParams(page=page, page_size=page_size)
    
    return await EstadoService.listar_estado_libro(db, pagination)


@estado_router.get("/prestamo", response_model=list[EstadoView] | PaginatedResponse[EstadoView])
async def listar_estados_prestamo(
    db: AsyncSession = Depends(get_session),
    page: int | None = Query(None, ge=1),
    page_size: int | None = Query(None, ge=1, le=100)
):
    """Listar estados de tipo prestamo
    Usa paginación si se proveen los parámetros page y page_size.
    """
    pagination = None
    if page is not None and page_size is not None:
        pagination = PaginationParams(page=page, page_size=page_size)
    
    return await EstadoService.listar_estado_prestamo(db, pagination)


@estado_router.get("/{id}", response_model=EstadoView)
async def obtener_estado(
    id: int,
    db: AsyncSession = Depends(get_session)
):
    """Obtener un estado por ID"""
    return await EstadoService.obtener_estado_id(id, db)


@estado_router.put("/{id}", response_model=EstadoView)
async def actualizar_estado(
    id: int,
    estado_update: EstadoUpdate,
    db: AsyncSession = Depends(get_session)
):
    """Actualizar un estado existente"""
    return await EstadoService.actualizar_estado(id, estado_update, db)


@estado_router.delete("/{id}", status_code=204)
async def eliminar_estado(
    id: int,
    db: AsyncSession = Depends(get_session)
):
    """Eliminar un estado"""
    await EstadoService.eliminar_estado(id, db)
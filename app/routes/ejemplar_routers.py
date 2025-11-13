from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.ejemplar_sch import (
    EjemplarCreate,
    EjemplarUpdate,
    EjemplarView,
    EjemplarReaderNormalized,
    EjemplarUpdateEstado,
)
from ..schemas.paginacion_sch import PaginationParams, PaginatedResponse
from ..services.ejemplar_service import EjemplarService
from ..core.db.postgre import get_session
from ..dependencies.auth import obtener_usuario_actual_administrador, obtener_usuario_actual_activo
from ..models.usuario import Usuario

ejemplar_router = APIRouter(prefix="/ejemplares", tags=["Ejemplares"])

@ejemplar_router.post("", response_model=EjemplarView, status_code=201)
async def crear_ejemplar(
    ejemplar: EjemplarCreate,
    db: AsyncSession = Depends(get_session),
    usuario_admin: Usuario = Depends(obtener_usuario_actual_administrador)
):
    """Crear un nuevo ejemplar"""
    return await EjemplarService.create_ejemplar(ejemplar, db)

@ejemplar_router.get("", response_model=list[EjemplarView] | list[EjemplarReaderNormalized] | PaginatedResponse[EjemplarView] | PaginatedResponse[EjemplarReaderNormalized])
async def listar_ejemplares(
    db: AsyncSession = Depends(get_session),
    page: int | None = Query(None, ge=1, description="Número de página"),
    page_size: int | None = Query(None, ge=1, le=100, description="Items por página"),
    normalizado: bool = Query(False, description="Retornar datos en formato normalizado")
):
    """
    Listar todos los ejemplares.
    Usa paginación si se proveen los parámetros page y page_size.
    """
    pagination = None
    if page is not None and page_size is not None:
        pagination = PaginationParams(page=page, page_size=page_size)
    
    return await EjemplarService.listar_ejemplares(db, pagination, normalizado)

@ejemplar_router.get("/{id}", response_model=EjemplarView)
async def obtener_ejemplar(
    id: int,
    db: AsyncSession = Depends(get_session),
    usuario_activo: Usuario = Depends(obtener_usuario_actual_activo)
):
    """Obtener un ejemplar por su ID"""
    return await EjemplarService.obtener_ejemplar(id, db)

@ejemplar_router.put("/{id}", response_model=EjemplarView)
async def actualizar_ejemplar(
    id: int,
    ejemplar_update: EjemplarUpdate,
    db: AsyncSession = Depends(get_session),
    usuario_admin: Usuario = Depends(obtener_usuario_actual_administrador)
):
    """Actualizar un ejemplar existente"""
    return await EjemplarService.actualizar_ejemplar(id, ejemplar_update, db)

@ejemplar_router.patch("/{id}/estado", response_model=EjemplarView)
async def actualizar_estado_ejemplar(
    id: int,
    estado_update: EjemplarUpdateEstado,
    db: AsyncSession = Depends(get_session),
    usuario_admin: Usuario = Depends(obtener_usuario_actual_administrador)
):
    """Actualizar el estado de un ejemplar"""
    return await EjemplarService.actualizar_estado_ejemplar(id, estado_update, db)

@ejemplar_router.delete("/{id}", response_model=dict)
async def eliminar_ejemplar(
    id: int,
    db: AsyncSession = Depends(get_session),
    usuario_admin: Usuario = Depends(obtener_usuario_actual_administrador)
):
    """Eliminar un ejemplar por su ID"""
    return await EjemplarService.eliminar_ejemplar(id, db)

@ejemplar_router.get("/codigo/{codigo_interno}", response_model=EjemplarView)
async def obtener_ejemplar_por_codigo(
    codigo_interno: str,
    db: AsyncSession = Depends(get_session),
    usuario_activo: Usuario = Depends(obtener_usuario_actual_activo)
):
    """Obtener un ejemplar por su código interno"""
    return await EjemplarService.obtener_ejemplar_por_codigo(codigo_interno, db)
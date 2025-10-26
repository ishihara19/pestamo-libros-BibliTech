from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.autor_sch import AutorCreate, AutorUpdate, AutorView
from ..schemas.paginacion_sch import PaginationParams, PaginatedResponse
from ..services.autor_service import AutorService
from ..schemas.generic_sch import GenericMessage
from ..core.db.postgre import get_session
from ..dependencies.auth import obtener_usuario_actual_administrador, obtener_usuario_actual_activo
from ..models.usuario import Usuario

autor_router = APIRouter(prefix="/autores", tags=["Autores"])


@autor_router.post("", response_model=AutorView, status_code=201)
async def crear_autor(
    autor: AutorCreate,
    db: AsyncSession = Depends(get_session),
    usuario_admin: Usuario = Depends(obtener_usuario_actual_administrador)
):
    """Crear un nuevo autor"""
    return await AutorService.create_autor(autor, db)

@autor_router.get("", response_model=list[AutorView] | PaginatedResponse[AutorView])
async def listar_autores(
    db: AsyncSession = Depends(get_session),
    page: int | None = Query(None, ge=1, description="Número de página"),
    page_size: int | None = Query(None, ge=1, le=100, description="Items por página")
):
    """
    Listar todos los autores.
    Usa paginación si se proveen los parámetros page y page_size.
    """
    pagination = None
    if page is not None and page_size is not None:
        pagination = PaginationParams(page=page, page_size=page_size)
    
    return await AutorService.listar_autores(db, pagination)

@autor_router.get("/{id}", response_model=AutorView)
async def obtener_autor_por_id(
    id: int,
    db: AsyncSession = Depends(get_session),
    usuario_activo: Usuario = Depends(obtener_usuario_actual_activo)
):
    """Obtener un autor por su ID"""
    return await AutorService.obtener_autor_por_id(id, db)

@autor_router.put("/{id}", response_model=AutorView)
async def actualizar_autor(
    id: int,
    autor: AutorUpdate,
    db: AsyncSession = Depends(get_session),
    usuario_admin: Usuario = Depends(obtener_usuario_actual_administrador)
):
    """Actualizar un autor por su ID"""
    return await AutorService.actualizar_autor(id, autor, db)

@autor_router.delete("/{id}", response_model=GenericMessage)
async def eliminar_autor(
    id: int,
    db: AsyncSession = Depends(get_session),
    usuario_admin: Usuario = Depends(obtener_usuario_actual_administrador)
):
    """Eliminar un autor por su ID"""
    return await AutorService.eliminar_autor(id, db)
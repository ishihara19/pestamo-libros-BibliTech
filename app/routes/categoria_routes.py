from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.categoria_sch import CategoriaCreate, CategoriaView, CategoriaUpdate
from ..schemas.paginacion_sch import PaginationParams, PaginatedResponse
from ..services.categoria_service import CategoriaService
from ..schemas.generic_sch import GenericMessage
from ..core.db.postgre import get_session
from ..dependencies.auth import obtener_usuario_actual_administrador, obtener_usuario_actual_activo
from ..models.usuario import Usuario

categoria_router = APIRouter(prefix="/categorias", tags=["Categorías"])

@categoria_router.post("", response_model=CategoriaView, status_code=201)
async def crear_categoria(
    categoria: CategoriaCreate,
    db: AsyncSession = Depends(get_session),
    usuario_admin: Usuario = Depends(obtener_usuario_actual_administrador)
):
    """Crear una nueva categoría"""
    return await CategoriaService.create_categoria(categoria, db)


@categoria_router.get("", response_model=list[CategoriaView] | PaginatedResponse[CategoriaView])
async def listar_categorias(
    db: AsyncSession = Depends(get_session),
    page: int | None = Query(None, ge=1, description="Número de página"),
    page_size: int | None = Query(None, ge=1, le=100, description="Items por página")
):
    """
    Listar todas las categorías.
    Usa paginación si se proveen los parámetros page y page_size.
    """
    pagination = None
    if page is not None and page_size is not None:
        pagination = PaginationParams(page=page, page_size=page_size)
    
    return await CategoriaService.listar_categorias(db, pagination)

@categoria_router.get("/{id}", response_model=CategoriaView)
async def obtener_categoria_por_id(
    id: int,
    db: AsyncSession = Depends(get_session),
    usuario_activo: Usuario = Depends(obtener_usuario_actual_activo)
):
    """Obtener una categoría por su ID"""
    return await CategoriaService.obtener_categoria_por_id(id, db)

@categoria_router.put("/{id}", response_model=CategoriaView)
async def actualizar_categoria(
    id: int,
    categoria: CategoriaUpdate,
    db: AsyncSession = Depends(get_session),
    usuario_admin: Usuario = Depends(obtener_usuario_actual_administrador)
):
    """Actualizar una categoría por su ID"""
    return await CategoriaService.actualizar_categoria(id, categoria, db)

@categoria_router.delete("/{id}", response_model=GenericMessage)
async def eliminar_categoria(
    id: int,
    db: AsyncSession = Depends(get_session),
    usuario_admin: Usuario = Depends(obtener_usuario_actual_administrador)
):
    """Eliminar una categoría por su ID"""
    return await CategoriaService.eliminar_categoria(id, db)
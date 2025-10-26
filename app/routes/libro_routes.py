from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.libro_sch import LibroCreate, LibroView, LibroUpdate, LibroViewNormalized
from ..schemas.paginacion_sch import PaginationParams, PaginatedResponse
from ..services.libro_service import LibroService
from ..schemas.generic_sch import GenericMessage
from ..core.db.postgre import get_session
from ..dependencies.auth import obtener_usuario_actual_administrador, obtener_usuario_actual_activo
from ..models.usuario import Usuario

libro_router = APIRouter(prefix="/libros", tags=["Libros"])

@libro_router.post("", response_model=LibroView, status_code=201)
async def crear_libro(
    libro: LibroCreate,
    db: AsyncSession = Depends(get_session),
    usuario_admin: Usuario = Depends(obtener_usuario_actual_administrador)
):
    """Crear un nuevo libro"""
    return await LibroService.create_libro(libro, db)

@libro_router.get("", response_model=list[LibroView] | list[LibroViewNormalized] | PaginatedResponse[LibroView] | PaginatedResponse[LibroViewNormalized])
async def listar_libros(
    db: AsyncSession = Depends(get_session),
    page: int | None = Query(None, ge=1, description="Número de página"),
    page_size: int | None = Query(None, ge=1, le=100, description="Items por página"),
    normalizado: bool = Query(False, description="Retornar libros en formato normalizado")
):
    """
    Listar todos los libros.
    Usa paginación si se proveen los parámetros page y page_size.
    El parámetro 'normalizado' indica si se debe retornar el formato normalizado.
    """
    pagination = None
    if page is not None and page_size is not None:
        pagination = PaginationParams(page=page, page_size=page_size)
    
    return await LibroService.listar_libros(db, pagination, normalizado)

@libro_router.get("/{id}", response_model=LibroView | LibroViewNormalized)
async def obtener_libro_por_id(
    id: int,
    db: AsyncSession = Depends(get_session),
    usuario_activo: Usuario = Depends(obtener_usuario_actual_activo),
    normalizado: bool = Query(False, description="Retornar libro en formato normalizado")
):
    """Obtener un libro por su ID"""
    return await LibroService.obtener_libro_por_id(id, db, normalizado)

@libro_router.put("/{id}", response_model=LibroView)
async def actualizar_libro(
    id: int,
    libro: LibroUpdate,
    db: AsyncSession = Depends(get_session),
    usuario_admin: Usuario = Depends(obtener_usuario_actual_administrador)
):
    """Actualizar un libro por su ID"""
    return await LibroService.actualizar_libro(id, libro, db)

@libro_router.delete("/{id}", response_model=GenericMessage)
async def eliminar_libro(
    id: int,
    db: AsyncSession = Depends(get_session),
    usuario_admin: Usuario = Depends(obtener_usuario_actual_administrador)
):
    """Eliminar un libro por su ID"""
    return await LibroService.eliminar_libro(id, db)

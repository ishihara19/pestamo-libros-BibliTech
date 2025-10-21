from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from ..schemas.tipo_documento_sch import TipoDocumentoCreate, TipoDocumentoView, TipoDocumentoUpdate
from ..schemas.paginacion_sch import PaginationParams, PaginatedResponse
from ..services.tipo_documento_service import TipoDocumentoService
from ..core.db.postgre import get_session

tipo_documento_router = APIRouter(prefix="/tipos-documento", tags=["Tipos de Documento"])

@tipo_documento_router.post("", response_model=TipoDocumentoView, status_code=201)
async def crear_tipo_documento(
    tipo_documento: TipoDocumentoCreate,
    db: AsyncSession = Depends(get_session)
):
    """Crear un nuevo tipo de documento"""
    return await TipoDocumentoService.create_tipo_documento(tipo_documento, db)

@tipo_documento_router.get("", response_model=list[TipoDocumentoView] | PaginatedResponse[TipoDocumentoView])
async def listar_tipos_documento(
    db: AsyncSession = Depends(get_session),
    page: int | None = Query(None, ge=1, description="Número de página"),
    page_size: int | None = Query(None, ge=1, le=100, description="Items por página")
):
    """
    Listar todos los tipos de documento.
    Usa paginación si se proveen los parámetros page y page_size.
    """
    pagination = None
    if page is not None and page_size is not None:
        pagination = PaginationParams(page=page, page_size=page_size)
    
    return await TipoDocumentoService.listar_tipos_documento(db, pagination)

@tipo_documento_router.get("/{id}", response_model=TipoDocumentoView)
async def obtener_tipo_documento(
    id: int,
    db: AsyncSession = Depends(get_session)
):
    """Obtener un tipo de documento por su ID"""
    tipo_documento =  await TipoDocumentoService.obtener_tipo_documento(id, db)
    if not tipo_documento:       
        raise HTTPException(status_code=404, detail="Tipo de documento no encontrado")
    return tipo_documento

@tipo_documento_router.put("/{id}", response_model=TipoDocumentoView)
async def actualizar_tipo_documento(
    id: int,
    tipo_documento_update: TipoDocumentoUpdate,
    db: AsyncSession = Depends(get_session)
):
    """Actualizar un tipo de documento existente"""
    return await TipoDocumentoService.actualizar_tipo_documento(id, tipo_documento_update, db)

@tipo_documento_router.delete("/{id}", status_code=204)
async def eliminar_tipo_documento(
    id: int,
    db: AsyncSession = Depends(get_session)
):
    """Eliminar un tipo de documento por su ID"""
    await TipoDocumentoService.eliminar_tipo_documento(id, db)

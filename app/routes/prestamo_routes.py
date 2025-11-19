from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from ..core.db.postgre import get_session
from ..schemas.paginacion_sch import PaginationParams, PaginatedResponse
from ..schemas.prestamo_sch import (
    HacerPrestamo,
    ConfirmarEntregaPrestamo,
)  # , PrestamoView, PrestamoReadNormalized
from ..schemas.generic_sch import GenericMessage
from ..services.prestamo_service import (
    PrestamoService,
    PrestamoViewBibliotecario,
    PrestamoViewNormalizedBibliotecario,
    PrestamoViewNormalizedLector,
)
from ..dependencies.auth import (
    obtener_usuario_actual_administrador,
    obtener_usuario_actual_activo,
    obtener_usuario_actual_administrador_o_bibliotecario,
)
from ..models.usuario import Usuario


prestamo_router = APIRouter(prefix="/prestamos", tags=["Préstamos"])


@prestamo_router.post("", response_model=GenericMessage, status_code=201)
async def crear_prestamo(
    prestamo_data: HacerPrestamo,
    db: AsyncSession = Depends(get_session),
    usuario: Usuario = Depends(obtener_usuario_actual_activo),
) -> GenericMessage:
    """Crear un nuevo préstamo"""
    ip = usuario.ip
    host = usuario.host
    username = usuario.username
    print(usuario.id)
    return await PrestamoService.crear_prestamo(
        db, prestamo_data, usuario.id, ip, host, username
    )


@prestamo_router.get(
    "",
    response_model=list[PrestamoViewBibliotecario]
    | list[PrestamoViewNormalizedBibliotecario]
    | PaginatedResponse[PrestamoViewBibliotecario]
    | PaginatedResponse[PrestamoViewNormalizedBibliotecario],
)
async def listar_prestamos(
    db: AsyncSession = Depends(get_session),
    page: int | None = Query(None, ge=1, description="Número de página"),
    page_size: int | None = Query(None, ge=1, le=100, description="Items por página"),
    normalizado: bool = Query(
        False, description="Retornar datos en formato normalizado"
    ),
    # usuario: Usuario = Depends(obtener_usuario_actual_administrador_o_bibliotecario)
):
    """
    Listar todos los préstamos.
    Usa paginación si se proveen los parámetros page y page_size.
    """
    pagination = None
    if page is not None and page_size is not None:
        pagination = PaginationParams(page=page, page_size=page_size)

    return await PrestamoService.listar_prestamos_bibliotecario(
        db, pagination, normalizado
    )


@prestamo_router.get(
    "/lector",
    response_model=list[PrestamoViewNormalizedLector]
    | PaginatedResponse[PrestamoViewNormalizedLector],
)
async def listar_prestamos_lector(
    db: AsyncSession = Depends(get_session),
    page: int | None = Query(None, ge=1, description="Número de página"),
    page_size: int | None = Query(None, ge=1, le=100, description="Items por página"),
    usuario: Usuario = Depends(obtener_usuario_actual_activo),
):
    """
    Listar todos los préstamos del lector actual.
    Usa paginación si se proveen los parámetros page y page_size.
    """
    pagination = None
    if page is not None and page_size is not None:
        pagination = PaginationParams(page=page, page_size=page_size)

    return await PrestamoService.listar_prestamos_lector(db, usuario.id, pagination)

@prestamo_router.post(
    "/confirmar-entrega",
    response_model=GenericMessage,
    status_code=200,
)
async def confirmar_entrega_prestamo(
    datos_prestamo: ConfirmarEntregaPrestamo,
    db: AsyncSession = Depends(get_session),
    usuario: Usuario = Depends(obtener_usuario_actual_administrador_o_bibliotecario),
) -> GenericMessage:
    """Confirmar la entrega de un préstamo por número de documento y código interno del ejemplar"""
    ip = usuario.ip
    host = usuario.host
    username = usuario.username
    return await PrestamoService.confirmar_entrega_por_documento(
        db, datos_prestamo, ip, host, username
    )
    

@prestamo_router.post(
    "/{codigo_interno}/confirmar-devolucion", 
    response_model=GenericMessage,
    status_code=200,
)
async def registrar_devolucion(
    codigo_interno: str,
    db: AsyncSession = Depends(get_session),
    usuario: Usuario = Depends(obtener_usuario_actual_administrador_o_bibliotecario),
) -> GenericMessage:
    """Confirmar la entrega de un préstamo por su ID"""
    ip = usuario.ip
    host = usuario.host
    username = usuario.username
    return await PrestamoService.registrar_devolucion(
        db, codigo_interno, ip, host, username
    )
    
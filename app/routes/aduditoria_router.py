from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from ..core.db.postgre import get_session
from ..schemas.paginacion_sch import PaginationParams, PaginatedResponse
from ..schemas.auditoria_sch import AuditoriaView
from ..services.auditoria_service import AuditoriaService
from ..dependencies.auth import obtener_usuario_actual_administrador

auditoria_router = APIRouter(prefix="/auditorias", tags=["Auditorías"])

@auditoria_router.get("", response_model=list[AuditoriaView] | PaginatedResponse[AuditoriaView])
async def listar_auditorias(
    db: AsyncSession = Depends(get_session),
    usuario_admin: bool = Depends(obtener_usuario_actual_administrador),
    page: int | None = Query(None, ge=1, description="Número de página (requiere page_size)"),
    page_size: int | None = Query(None, ge=1, le=100, description="Items por página (requiere page)"),
    tabla: str | None = Query(
        None, 
        description="Filtrar por tabla exacta. Ejemplos válidos:\n"
            "- usuario\n"
            "- ejemplar\n"
            "- prestamo",
        max_length=100
    ),
    operacion: str | None = Query(
        None, 
        description="Filtrar por operación (búsqueda parcial). Ejemplos válidos:\n"
            "- insert\n"
            "- update\n"
            "- delete",
        max_length=50
    ),
    desde_fecha: str | None = Query(
        None, 
        description="Fecha inicial (ISO 8601). Ejemplos:\n"
            "- 2025-01-15\n"
            "- 2025-01-15T10:30:00",
        pattern=r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2})?$"
    ),
    hasta_fecha: str | None = Query(
        None, 
        description="Fecha final (ISO 8601). Ejemplos:\n"
            "- 2025-01-31\n"
            "- 2025-01-31T23:59:59",
        pattern=r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2})?$"
    ),
    usuario_app: str | None = Query(
        None, 
        description="Filtrar por usuario de la aplicación (búsqueda parcial, case-insensitive)",
        max_length=100
    ),
    operacion_app: str | None = Query(
        None, 
        description="Filtrar por operación de la aplicación (búsqueda parcial, case-insensitive)",
        max_length=100
    ),
):
    """
    Listar registros de auditoría con filtros opcionales.
    
    **Paginación:**
    - Si se proveen `page` y `page_size`, retorna respuesta paginada
    - Si se omiten, retorna todos los registros (sin paginación)
    
    **Filtros:**
    - `tabla`: Búsqueda exacta del nombre de la tabla\n
    - `operacion`: Búsqueda parcial de la operación SQL (insert, update, delete)
    - `desde_fecha` / `hasta_fecha`: Rango de fechas en formato ISO 8601
    - `usuario_app`: Búsqueda parcial del usuario (case-insensitive)
    - `operacion_app`: Búsqueda parcial de la operación de la app (case-insensitive)
    
    **Orden:**
    - Los registros se ordenan por fecha de operación descendente (más recientes primero)
    """
    # Validar que ambos parámetros de paginación estén presentes o ambos ausentes
    if (page is None) != (page_size is None):
        raise HTTPException(
            status_code=400,
            detail="Los parámetros 'page' y 'page_size' deben proporcionarse juntos o no usarse"
        )
    
    pagination = None
    if page is not None and page_size is not None:
        pagination = PaginationParams(page=page, page_size=page_size)
    
    return await AuditoriaService.listar_auditorias(
        db,
        pagination,
        tabla,
        operacion,
        desde_fecha,
        hasta_fecha,
        usuario_app,
        operacion_app
    )
    
@auditoria_router.get("/{id}", response_model=AuditoriaView)
async def obtener_auditoria(
    id: int,
    db: AsyncSession = Depends(get_session),
    usuario_admin: bool = Depends(obtener_usuario_actual_administrador),
):
    """Obtener un registro de auditoría por su ID"""
    auditoria = await AuditoriaService.obtener_auditoria(id, db)
    if not auditoria:
        raise HTTPException(status_code=404, detail="Registro de auditoría no encontrado")
    return auditoria
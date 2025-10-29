from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException
from datetime import datetime

from ..models.auditoria import Auditoria
from ..schemas.auditoria_sch import AuditoriaView
from ..schemas.paginacion_sch import PaginationParams, PaginatedResponse


class AuditoriaService:
    
    @staticmethod
    async def listar_auditorias(
        db: AsyncSession, 
        pagination: PaginationParams | None = None,
        tabla: str | None = None,
        operacion: str | None = None,
        desde_fecha: str | None = None,
        hasta_fecha: str | None = None,
        usuario_app: str | None = None,
        operacion_app: str | None = None,
    ) -> list[AuditoriaView] | PaginatedResponse[AuditoriaView]:
        """
        Listar todos los registros de auditoría con filtros opcionales.
        Si se proveen parámetros de paginación, retorna una respuesta paginada.
        Permite búsqueda parcial en usuario_app y operacion_app.
        """

        # --- Construir filtros reutilizables ---
        filters = []
        
        if tabla:
            tabla_escaped = tabla.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
            filters.append(Auditoria.tabla.ilike(f"%{tabla_escaped}%"))

        if operacion:
            # Escapar caracteres especiales de LIKE para evitar búsquedas inesperadas
            operacion_escaped = operacion.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
            filters.append(Auditoria.operacion.ilike(f"%{operacion_escaped}%"))

        # Conversión segura de fechas
        if desde_fecha:
            try:
                desde_fecha_dt = datetime.fromisoformat(desde_fecha)
                filters.append(Auditoria.fecha_operacion >= desde_fecha_dt)
            except ValueError:
                raise ValueError("El formato de 'desde_fecha' no es válido. Usa ISO 8601 (YYYY-MM-DD o YYYY-MM-DDTHH:MM:SS).")
        
        if hasta_fecha:
            try:
                hasta_fecha_dt = datetime.fromisoformat(hasta_fecha)
                filters.append(Auditoria.fecha_operacion <= hasta_fecha_dt)
            except ValueError:
                raise ValueError("El formato de 'hasta_fecha' no es válido. Usa ISO 8601 (YYYY-MM-DD o YYYY-MM-DDTHH:MM:SS).")

        # Búsqueda parcial (case-insensitive) con escape de caracteres LIKE
        if usuario_app:
            usuario_app_escaped = usuario_app.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
            filters.append(Auditoria.usuario_app.ilike(f"%{usuario_app_escaped}%"))
        
        if operacion_app:
            operacion_app_escaped = operacion_app.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
            filters.append(Auditoria.operacion_app.ilike(f"%{operacion_app_escaped}%"))

        # Query principal con filtros
        query = select(Auditoria).where(*filters).order_by(Auditoria.fecha_operacion.desc())

        # --- Paginación ---
        if pagination:
            # Contar total (reutilizando los mismos filtros)
            count_query = select(func.count()).select_from(Auditoria).where(*filters)
            total = (await db.execute(count_query)).scalar()

            # Obtener registros paginados
            result = await db.execute(
                query.offset(pagination.offset).limit(pagination.limit)
            )
            auditorias = result.scalars().all()

            items = [AuditoriaView.model_validate(a) for a in auditorias]
            return PaginatedResponse.create(items, total, pagination)

        # --- Sin paginación ---
        result = await db.execute(query)
        auditorias = result.scalars().all()
        return [AuditoriaView.model_validate(a) for a in auditorias]


@staticmethod
async def obtener_auditoria_por_id(
    auditoria_id: int, 
    db: AsyncSession
) -> AuditoriaView:
    """Obtener un registro de auditoría por su ID."""
    result = await db.execute(select(Auditoria).where(Auditoria.id == auditoria_id))
    auditoria = result.scalar_one_or_none()
    if not auditoria:
        raise HTTPException(status_code=404, detail="Auditoría no encontrada")
    return AuditoriaView.model_validate(auditoria)
        
    
    @staticmethod
    async def obtener_auditoria_por_id(
        auditoria_id: int, 
        db: AsyncSession
    ) -> AuditoriaView:
        """Obtener un registro de auditoría por su ID."""
        result = await db.execute(select(Auditoria).where(Auditoria.id == auditoria_id))
        auditoria = result.scalar_one_or_none()
        if not auditoria:
            raise HTTPException(status_code=404, detail="Auditoría no encontrada")
        return AuditoriaView.model_validate(auditoria)
    

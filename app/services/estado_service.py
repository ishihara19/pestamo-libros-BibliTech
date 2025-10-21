from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException

from ..models.estado import Estado
from ..schemas.estado_sch import EstadoCreate, EstadoUpdate, EstadoView
from ..schemas.paginacion_sch import PaginationParams, PaginatedResponse


class EstadoService:
    """Servicio para manejar operaciones relacionadas con el modelo Estado."""
    
    @staticmethod
    async def create_estado(estado: EstadoCreate, db: AsyncSession) -> EstadoView:
        """Crear un nuevo estado en la base de datos."""
        nuevo_estado = Estado(**estado.model_dump())
        db.add(nuevo_estado)
        await db.commit()
        await db.refresh(nuevo_estado)
        return EstadoView.model_validate(nuevo_estado)

    @staticmethod
    async def listar_estados(
        db: AsyncSession, 
        pagination: PaginationParams | None = None
    ) -> list[EstadoView] | PaginatedResponse[EstadoView]:
        """
        Listar todos los estados en la base de datos.
        Si se proveen parámetros de paginación, retorna una respuesta paginada.
        """
        if pagination:
            # Contar total de registros
            count_query = select(func.count(Estado.id))
            total_result = await db.execute(count_query)
            total = total_result.scalar()
            
            # Obtener registros paginados
            query = (
                select(Estado)
                .offset(pagination.offset)
                .limit(pagination.limit)
            )
            result = await db.execute(query)
            estados = result.scalars().all()
            
            items = [EstadoView.model_validate(estado) for estado in estados]
            return PaginatedResponse.create(items, total, pagination)
        
        # Sin paginación (comportamiento original)
        result = await db.execute(select(Estado))
        estados = result.scalars().all()
        return [EstadoView.model_validate(estado) for estado in estados]
    
    
    @staticmethod
    async def listar_estado_por_tipo(
        db: AsyncSession,
        tipo: str,
        pagination: PaginationParams | None = None
    ) -> list[EstadoView] | PaginatedResponse[EstadoView]:
        """Listar estados por tipo con paginación opcional."""
        base_query = select(Estado).where(Estado.tipo == tipo)
        
        if pagination:
            # Contar total
            count_query = select(func.count(Estado.id)).where(Estado.tipo == tipo)
            total_result = await db.execute(count_query)
            total = total_result.scalar()
            
            # Paginar
            query = base_query.offset(pagination.offset).limit(pagination.limit)
            result = await db.execute(query)
            estados = result.scalars().all()
            
            items = [EstadoView.model_validate(estado) for estado in estados]
            return PaginatedResponse.create(items, total, pagination)
        
        result = await db.execute(base_query)
        estados = result.scalars().all()
        return [EstadoView.model_validate(estado) for estado in estados]
        
    @staticmethod
    async def obtener_estado_id(id: int, db: AsyncSession) -> EstadoView:
        """Obtener un estado por su ID."""
        result = await db.execute(select(Estado).where(Estado.id == id))
        estado = result.scalar_one_or_none()
        if not estado:
            raise HTTPException(status_code=404, detail="Estado no encontrado")
        return EstadoView.model_validate(estado)
    
    @staticmethod
    async def actualizar_estado(id: int, estado_update: EstadoUpdate, db: AsyncSession) -> EstadoView:
        """Actualizar un estado existente."""
        result = await db.execute(select(Estado).where(Estado.id == id))
        estado = result.scalar_one_or_none()
        if not estado:
            raise HTTPException(status_code=404, detail="Estado no encontrado")
        
        for key, value in estado_update.model_dump(exclude_unset=True).items():
            setattr(estado, key, value)
        
        await db.commit()
        await db.refresh(estado)
        return EstadoView.model_validate(estado)
    
    @staticmethod
    async def eliminar_estado(id: int, db: AsyncSession) -> None:
        """Eliminar un estado por su ID."""
        result = await db.execute(select(Estado).where(Estado.id == id))
        estado = result.scalar_one_or_none()
        if not estado:
            raise HTTPException(status_code=404, detail="Estado no encontrado")
        
        await db.delete(estado)
        await db.commit()
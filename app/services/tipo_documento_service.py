from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException

from ..models.tipo_documento import TipoDocumento
from ..schemas.tipo_documento_sch import TipoDocumentoCreate, TipoDocumentoUpdate, TipoDocumentoView
from ..schemas.paginacion_sch import PaginationParams, PaginatedResponse


class TipoDocumentoService:
    """Servicio para manejar operaciones relacionadas con el modelo TipoDocumento."""
    
    @staticmethod
    async def create_tipo_documento(tipo_documento: TipoDocumentoCreate, db: AsyncSession) -> TipoDocumentoView:
        """Crear un nuevo tipo de documento en la base de datos."""
        nuevo_tipo_documento = TipoDocumento(**tipo_documento.model_dump())
        db.add(nuevo_tipo_documento)
        await db.commit()
        await db.refresh(nuevo_tipo_documento)
        return TipoDocumentoView.model_validate(nuevo_tipo_documento)

    @staticmethod
    async def listar_tipos_documento(
        db: AsyncSession, 
        pagination: PaginationParams | None = None
    ) -> list[TipoDocumentoView] | PaginatedResponse[TipoDocumentoView]:
        """
        Listar todos los tipos de documento en la base de datos.
        Si se proveen parámetros de paginación, retorna una respuesta paginada.
        """
        if pagination:
            # Contar total de registros
            count_query = select(func.count(TipoDocumento.id))
            total_result = await db.execute(count_query)
            total = total_result.scalar()
            
            # Obtener registros paginados
            query = (
                select(TipoDocumento)
                .offset(pagination.offset)
                .limit(pagination.limit)
            )
            result = await db.execute(query)
            tipos_documento = result.scalars().all()
            
            items = [TipoDocumentoView.model_validate(tipo) for tipo in tipos_documento]
            return PaginatedResponse.create(items, total, pagination)
        
        # Sin paginación (comportamiento original)
        result = await db.execute(select(TipoDocumento))
        tipos_documento = result.scalars().all()
        return [TipoDocumentoView.model_validate(tipo) for tipo in tipos_documento]
    
    @staticmethod
    async def obtener_tipo_documento(id: int, db: AsyncSession) -> TipoDocumentoView | None:
        """Obtener un tipo de documento por su ID."""
        result = await db.execute(select(TipoDocumento).where(TipoDocumento.id == id))
        tipo_documento = result.scalar()
        return TipoDocumentoView.model_validate(tipo_documento) if tipo_documento else None
    
    @staticmethod
    async def actualizar_tipo_documento(
        id: int, 
        tipo_documento_update: TipoDocumentoUpdate, 
        db: AsyncSession
    ) -> TipoDocumentoView:
        """Actualizar un tipo de documento existente."""
        result = await db.execute(select(TipoDocumento).where(TipoDocumento.id == id))
        tipo_documento = result.scalar()
        
        if not tipo_documento:
            raise HTTPException(status_code=404, detail="Tipo de documento no encontrado")
        
        for var, value in tipo_documento_update.model_dump(exclude_unset=True).items():
            setattr(tipo_documento, var, value)
        
        db.add(tipo_documento)
        await db.commit()
        await db.refresh(tipo_documento)
        
        return TipoDocumentoView.model_validate(tipo_documento)
    
    @staticmethod
    async def eliminar_tipo_documento(id: int, db: AsyncSession) -> None:
        """Eliminar un tipo de documento por su ID."""
        result = await db.execute(select(TipoDocumento).where(TipoDocumento.id == id))
        tipo_documento = result.scalar()
        
        if not tipo_documento:
            raise HTTPException(status_code=404, detail="Tipo de documento no encontrado")
        
        await db.delete(tipo_documento)
        await db.commit()
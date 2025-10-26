from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException

from ..models.autor import Autor
from ..schemas.autor_sch import AutorCreate, AutorUpdate, AutorView
from ..schemas.paginacion_sch import PaginationParams, PaginatedResponse
from ..schemas.generic_sch import GenericMessage

class AutorService:
    
    @staticmethod
    async def create_autor(autor: AutorCreate, db: AsyncSession) -> AutorView:
        """Crear un nuevo autor en la base de datos."""
        nuevo_autor = Autor(**autor.model_dump())
        db.add(nuevo_autor)
        await db.commit()
        await db.refresh(nuevo_autor)
        return AutorView.model_validate(nuevo_autor)
    
    @staticmethod
    async def listar_autores(
        db: AsyncSession, 
        pagination: PaginationParams | None = None
    ) -> list[AutorView] | PaginatedResponse[AutorView]:
        """
        Listar todos los autores en la base de datos.
        Si se proveen parámetros de paginación, retorna una respuesta paginada.
        """
        if pagination:
            # Contar total de registros
            count_query = select(func.count(Autor.id))
            total_result = await db.execute(count_query)
            total = total_result.scalar()
            
            # Obtener registros paginados
            query = (
                select(Autor)
                .offset(pagination.offset)
                .limit(pagination.limit)
            )
            result = await db.execute(query)
            autores = result.scalars().all()
            
            items = [AutorView.model_validate(autor) for autor in autores]
            return PaginatedResponse.create(items, total, pagination)
        
        # Sin paginación (comportamiento original)
        result = await db.execute(select(Autor))
        autores = result.scalars().all()
        return [AutorView.model_validate(autor) for autor in autores]
    

    @staticmethod
    async def obtener_autor_por_id(
        autor_id: int, 
        db: AsyncSession
    ) -> AutorView:
        """Obtener un autor por su ID."""
        result = await db.execute(select(Autor).where(Autor.id == autor_id))
        autor = result.scalar_one_or_none()
        
        if not autor:
            raise HTTPException(status_code=404, detail="Autor no encontrado")
        
        return AutorView.model_validate(autor)
    
    @staticmethod
    async def actualizar_autor(
        autor_id: int, 
        autor_update: AutorUpdate, 
        db: AsyncSession
    ) -> AutorView:
        """Actualizar un autor existente en la base de datos."""
        result = await db.execute(select(Autor).where(Autor.id == autor_id))
        autor = result.scalar_one_or_none()
        
        if not autor:
            raise HTTPException(status_code=404, detail="Autor no encontrado")
        
        for var, value in autor_update.model_dump(exclude_unset=True).items():
            setattr(autor, var, value)
        
        db.add(autor)
        await db.commit()
        await db.refresh(autor)
        return AutorView.model_validate(autor)
    
    @staticmethod
    async def eliminar_autor(
        autor_id: int, 
        db: AsyncSession
    ) -> GenericMessage:
        """Eliminar un autor de la base de datos."""
        result = await db.execute(select(Autor).where(Autor.id == autor_id))
        autor = result.scalar_one_or_none()
        
        if not autor:
            raise HTTPException(status_code=404, detail="Autor no encontrado")
        
        await db.delete(autor)
        await db.commit()
        return GenericMessage(message="Autor eliminado con éxito")
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException
from sqlalchemy.orm import selectinload

from ..models.ejemplar import Ejemplar
from ..schemas.ejemplar_sch import (
    EjemplarCreate,
    EjemplarUpdate,
    EjemplarView,
    EjemplarReaderNormalized,
    EjemplarUpdateEstado,
)
from ..schemas.paginacion_sch import PaginationParams, PaginatedResponse
from ..schemas.generic_sch import GenericMessage
from ..utils.utils import generar_codigo_unico

class EjemplarService:
    @staticmethod
    async def create_ejemplar(ejemplar: EjemplarCreate, db: AsyncSession) -> EjemplarView:
        """Crear un nuevo ejemplar en la base de datos."""
        nuevo_ejemplar = Ejemplar(**ejemplar.model_dump())
        codigo = await generar_codigo_unico(nuevo_ejemplar.libro_id, db)
        nuevo_ejemplar.codigo_interno = codigo
        db.add(nuevo_ejemplar)
        await db.commit()
        await db.refresh(nuevo_ejemplar)
        return EjemplarView.model_validate(nuevo_ejemplar)

    @staticmethod
    async def listar_ejemplares(
        db: AsyncSession,
        pagination: PaginationParams | None = None,
        normalizado: bool = False,
    ) -> (
        list[EjemplarView]
        | list[EjemplarReaderNormalized]
        | PaginatedResponse[EjemplarView]
        | PaginatedResponse[EjemplarReaderNormalized]
    ):
        """
        Listar todos los ejemplares en la base de datos.
        Si se proveen parámetros de paginación, retorna una respuesta paginada.
        """
        if pagination:
            # Contar total de registros
            count_query = select(func.count(Ejemplar.id))
            total_result = await db.execute(count_query)
            total = total_result.scalar()
            if normalizado:
                # Obtener registros paginados
                query = (
                    select(Ejemplar)
                    .options(selectinload(Ejemplar.libro), selectinload(Ejemplar.estado))
                    .offset(pagination.offset)
                    .limit(pagination.limit)
                )
                result = await db.execute(query)
                ejemplares = result.scalars().all()

                items = [EjemplarReaderNormalized.from_model(ejemplar) for ejemplar in ejemplares]
                return PaginatedResponse.create(items, total, pagination)
            # Obtener registros paginados
            query = select(Ejemplar).offset(pagination.offset).limit(pagination.limit)
            result = await db.execute(query)
            ejemplares = result.scalars().all()

            items = [EjemplarView.model_validate(ejemplar) for ejemplar in ejemplares]
            return PaginatedResponse.create(items, total, pagination)
        
        # Sin paginación (comportamiento original)
        if normalizado:
            result = await db.execute(
                select(Ejemplar).options(selectinload(Ejemplar.libro), selectinload(Ejemplar.estado))
            )
            ejemplares = result.scalars().all()
            return [EjemplarReaderNormalized.from_model(ejemplar) for ejemplar in ejemplares]   
        result = await db.execute(select(Ejemplar))
        ejemplares = result.scalars().all()
        return [EjemplarView.model_validate(ejemplar) for ejemplar in ejemplares]
    
    @staticmethod
    async def actualizar_estado_ejemplar(       
        ejemplar_id: int,
        estado_update: EjemplarUpdateEstado,
        db: AsyncSession
    ) -> GenericMessage:
        """Actualizar el estado de un ejemplar."""
        query = select(Ejemplar).where(Ejemplar.id == ejemplar_id)
        result = await db.execute(query)
        ejemplar = result.scalar_one_or_none()

        if not ejemplar:
            raise HTTPException(status_code=404, detail="Ejemplar no encontrado")

        ejemplar.estado_id = estado_update.estado_id
        if estado_update.actualizado_en:
            ejemplar.actualizado_en = estado_update.actualizado_en

        db.add(ejemplar)
        await db.commit()
        return GenericMessage(message="Estado del ejemplar actualizado correctamente")
    
    @staticmethod
    async def obtener_ejemplar_por_id(
        ejemplar_id: int, db: AsyncSession, normalizado: bool
    ) -> EjemplarView | EjemplarReaderNormalized:
        """Obtener un ejemplar por su ID."""
        if normalizado:
            result = await db.execute(
                select(Ejemplar)
                .options(selectinload(Ejemplar.libro), selectinload(Ejemplar.estado))
                .where(Ejemplar.id == ejemplar_id)
            )
            ejemplar = result.scalar()
            if not ejemplar:
                raise HTTPException(status_code=404, detail="Ejemplar no encontrado")
            return EjemplarReaderNormalized.from_model(ejemplar)
        result = await db.execute(
                select(Ejemplar)
                .options(
                    selectinload(Ejemplar.libro),
                    selectinload(Ejemplar.estado)
                )
                .where(Ejemplar.id == ejemplar_id)
            )

        ejemplar = result.scalar()
        if not ejemplar:
            raise HTTPException(status_code=404, detail="Ejemplar no encontrado")
        return EjemplarView.model_validate(ejemplar)
    
    @staticmethod
    async def actualizar_ejemplar(
        ejemplar_id: int, ejemplar_update: EjemplarUpdate, db: AsyncSession
    ) -> EjemplarView:
        """Actualizar un ejemplar existente por su ID."""
        result = await db.execute(select(Ejemplar).where(Ejemplar.id == ejemplar_id))
        ejemplar = result.scalar_one_or_none()

        if not ejemplar:
            raise HTTPException(status_code=404, detail="Ejemplar no encontrado")

        for var, value in ejemplar_update.model_dump(exclude_unset=True).items():
            setattr(ejemplar, var, value)

        db.add(ejemplar)
        await db.commit()
        await db.refresh(ejemplar)

        return EjemplarView.model_validate(ejemplar)
    
    @staticmethod
    async def eliminar_ejemplar(ejemplar_id: int, db: AsyncSession) -> GenericMessage:
        """Eliminar un ejemplar por su ID."""
        result = await db.execute(select(Ejemplar).where(Ejemplar.id == ejemplar_id))
        ejemplar = result.scalar_one_or_none()

        if not ejemplar:
            raise HTTPException(status_code=404, detail="Ejemplar no encontrado")

        await db.delete(ejemplar)
        await db.commit()

        return GenericMessage(message="Ejemplar eliminado correctamente")
    
    async def obtener_ejemplar_por_codigo(
        codigo_interno: str, db: AsyncSession
    ) -> EjemplarReaderNormalized:
        """Obtener un ejemplar por su código interno."""
        result = await db.execute(
            select(Ejemplar)
            .options(
                selectinload(Ejemplar.libro),
                selectinload(Ejemplar.estado)
            )
            .where(Ejemplar.codigo_interno == codigo_interno)
        )
        ejemplar = result.scalar_one_or_none()

        if not ejemplar:
            raise HTTPException(status_code=404, detail="Ejemplar no encontrado")

        return EjemplarReaderNormalized.from_model(ejemplar)
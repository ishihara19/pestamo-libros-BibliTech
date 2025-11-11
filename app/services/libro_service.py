from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException
from sqlalchemy.orm import selectinload

from ..models.libro import Libro
from ..schemas.libro_sch import LibroCreate, LibroUpdate, LibroView, LibroViewNormalized,  LibroURLUpdate
from ..schemas.paginacion_sch import PaginationParams, PaginatedResponse
from ..schemas.generic_sch import GenericMessage

class LibroService:
    @staticmethod
    async def create_libro(libro: LibroCreate, db: AsyncSession, imagen_url: str) -> LibroView:
        """Crear un nuevo libro en la base de datos."""
        nuevo_libro = Libro(**libro.model_dump(), imagen_url=imagen_url)
        db.add(nuevo_libro)
        await db.commit()
        await db.refresh(nuevo_libro)
        return LibroView.model_validate(nuevo_libro)

    @staticmethod
    async def listar_libros(
        db: AsyncSession,
        pagination: PaginationParams | None = None,
        normalizado: bool = False,
    ) -> (
        list[LibroView]
        | list[LibroViewNormalized]
        | PaginatedResponse[LibroView]
        | PaginatedResponse[LibroViewNormalized]
    ):
        """
        Listar todos los libros en la base de datos.
        Si se proveen parámetros de paginación, retorna una respuesta paginada.
        """
        if pagination:
            # Contar total de registros
            count_query = select(func.count(Libro.id))
            total_result = await db.execute(count_query)
            total = total_result.scalar()
            if normalizado:
                # Obtener registros paginados
                query = (
                    select(Libro)
                    .options(selectinload(Libro.categoria))
                    .offset(pagination.offset)
                    .limit(pagination.limit)
                )
                result = await db.execute(query)
                libros = result.scalars().all()

                items = [LibroViewNormalized.from_model(libro) for libro in libros]
                return PaginatedResponse.create(items, total, pagination)
            # Obtener registros paginados
            query = select(Libro).offset(pagination.offset).limit(pagination.limit)
            result = await db.execute(query)
            libros = result.scalars().all()

            items = [LibroView.model_validate(libro) for libro in libros]
            return PaginatedResponse.create(items, total, pagination)

        # Sin paginación (comportamiento original)
        if normalizado:
            result = await db.execute(
                select(Libro).options(selectinload(Libro.categoria))
            )
            libros = result.scalars().all()
            return [LibroViewNormalized.from_model(libro) for libro in libros]
        result = await db.execute(select(Libro))
        libros = result.scalars().all()
        return [LibroView.model_validate(libro) for libro in libros]

    @staticmethod
    async def obtener_libro_por_id(
        libro_id: int, db: AsyncSession, normalizado: bool
    ) -> LibroView | LibroViewNormalized:
        """Obtener un libro por su ID."""
        if normalizado:
            result = await db.execute(
                select(Libro)
                .options(selectinload(Libro.categoria))
                .where(Libro.id == libro_id)
            )
            libro = result.scalar()
            if not libro:
                raise HTTPException(status_code=404, detail="Libro no encontrado")
            return LibroViewNormalized.from_model(libro)
        result = await db.execute(select(Libro).where(Libro.id == libro_id))
        libro = result.scalar()
        if not libro:
            raise HTTPException(status_code=404, detail="Libro no encontrado")
        return LibroView.model_validate(libro)

    @staticmethod
    async def actualizar_libro(
        libro_id: int, libro_update: LibroUpdate, db: AsyncSession
    ) -> LibroView:
        """Actualizar un libro existente por su ID."""
        result = await db.execute(select(Libro).where(Libro.id == libro_id))
        libro = result.scalar_one_or_none()

        if not libro:
            raise HTTPException(status_code=404, detail="Libro no encontrado")

        for var, value in libro_update.model_dump(exclude_unset=True).items():
            setattr(libro, var, value)

        db.add(libro)
        await db.commit()
        await db.refresh(libro)

        return LibroView.model_validate(libro)

    @staticmethod
    async def eliminar_libro(libro_id: int, db: AsyncSession) -> GenericMessage:
        """Eliminar un libro por su ID."""
        result = await db.execute(select(Libro).where(Libro.id == libro_id))
        libro = result.scalar_one_or_none()

        if not libro:
            raise HTTPException(status_code=404, detail="Libro no encontrado")

        await db.delete(libro)
        await db.commit()

        return GenericMessage(message="Libro eliminado exitosamente")

    @staticmethod
    async def actualizar_imagen_libro(
        libro_id: int, imagen_url: LibroURLUpdate, db: AsyncSession
    ) -> LibroURLUpdate:
        """Actualizar la URL de la imagen de un libro por su ID."""
        result = await db.execute(select(Libro).where(Libro.id == libro_id))
        libro = result.scalar_one_or_none()

        if not libro:
            raise HTTPException(status_code=404, detail="Libro no encontrado")

        libro.imagen_url = imagen_url
        db.add(libro)
        await db.commit()
        await db.refresh(libro)

        return LibroURLUpdate(imagen_url=libro.imagen_url)
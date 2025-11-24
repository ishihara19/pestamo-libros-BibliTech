from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException
from sqlalchemy.orm import selectinload
from sqlalchemy import case

from ..models.libro import Libro
from ..models.autor import Autor
from ..models.ejemplar import Ejemplar
from ..schemas.libro_sch import LibroCreate, LibroUpdate, LibroView, LibroViewNormalized,  LibroURLUpdate
from ..core.config import settings
from ..schemas.paginacion_sch import PaginationParams, PaginatedResponse
from ..schemas.generic_sch import GenericMessage

class LibroService:
    @staticmethod
    async def create_libro(libro: LibroCreate, db: AsyncSession, imagen_url: str) -> LibroView:
        """Crear un nuevo libro en la base de datos."""
        data = libro.model_dump()
        autores_ids = data.pop("autores_ids", None)
        nuevo_libro = Libro(**data, imagen_url=imagen_url)
        # vincular autores si se proporcionan ids
        if autores_ids:
            result = await db.execute(select(Autor).where(Autor.id.in_(autores_ids)))
            autores = result.scalars().all()
            found_ids = {a.id for a in autores}
            missing = set(autores_ids) - found_ids
            if missing:
                raise HTTPException(status_code=400, detail=f"Autores no encontrados: {sorted(list(missing))}")
            nuevo_libro.autores = autores
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
                    .options(
                        selectinload(Libro.categoria),
                        selectinload(Libro.autores),
                    )
                    .offset(pagination.offset)
                    .limit(pagination.limit)
                )
                result = await db.execute(query)
                libros = result.scalars().all()

                # calcular counts por libro sin cargar los ejemplares completos
                libro_ids = [l.id for l in libros]
                counts_map = {}
                if libro_ids:
                    counts_stmt = (
                        select(
                            Ejemplar.libro_id,
                            func.count(Ejemplar.id).label("total"),
                            func.sum(case((Ejemplar.estado_id == settings.DISPONIBILIDAD_EJEMPLAR_DISPONIBLE_ID, 1), else_=0)).label("disponible"),
                            func.sum(case((Ejemplar.estado_id == settings.RESERVADO_EJEMPLAR_ID, 1), else_=0)).label("reservado"),
                            func.sum(case((Ejemplar.estado_id == settings.PRESTADO_EJEMPLAR_NO_DISPONIBLE_ID, 1), else_=0)).label("prestado"),
                            func.sum(case((Ejemplar.estado_id == 6, 1), else_=0)).label("danado"),
                        )
                        .where(Ejemplar.libro_id.in_(libro_ids))
                        .group_by(Ejemplar.libro_id)
                    )
                    counts_result = await db.execute(counts_stmt)
                    counts_rows = counts_result.all()
                    counts_map = {r.libro_id: r._asdict() for r in counts_rows}

                items = []
                for libro in libros:
                    item = LibroViewNormalized.from_model(libro)
                    c = counts_map.get(libro.id, {})
                    item.ejemplares_count = int(c.get("total", 0))
                    item.ejemplares_disponibles = int(c.get("disponible", 0))
                    item.ejemplares_reservados = int(c.get("reservado", 0))
                    item.ejemplares_prestados = int(c.get("prestado", 0))
                    item.ejemplares_danados = int(c.get("danado", 0))
                    items.append(item)
                return PaginatedResponse.create(items, total, pagination)
            # Obtener registros paginados
            query = (
                select(Libro)
                .options(selectinload(Libro.autores), selectinload(Libro.ejemplar))
                .offset(pagination.offset)
                .limit(pagination.limit)
            )
            result = await db.execute(query)
            libros = result.scalars().all()

            # obtener conteos de ejemplares por libro en una sola consulta
            libro_ids = [l.id for l in libros]
            counts_stmt = (
                select(
                    Ejemplar.libro_id,
                    func.count(Ejemplar.id).label("total"),
                    func.sum(case((Ejemplar.estado_id == settings.DISPONIBILIDAD_EJEMPLAR_DISPONIBLE_ID, 1), else_=0)).label("disponible"),
                    func.sum(case((Ejemplar.estado_id == settings.RESERVADO_EJEMPLAR_ID, 1), else_=0)).label("reservado"),
                    func.sum(case((Ejemplar.estado_id == settings.PRESTADO_EJEMPLAR_NO_DISPONIBLE_ID, 1), else_=0)).label("prestado"),
                    func.sum(case((Ejemplar.estado_id == 6, 1), else_=0)).label("danado"),
                )
                .where(Ejemplar.libro_id.in_(libro_ids))
                .group_by(Ejemplar.libro_id)
            )
            counts_result = await db.execute(counts_stmt)
            counts_rows = counts_result.all()
            counts_map = {r.libro_id: r._asdict() for r in counts_rows}

            items = []
            from ..schemas.autor_sch import AutorSimpleView
            for libro in libros:
                item = LibroView.model_validate(libro)
                item.autores = [AutorSimpleView.model_validate(a) for a in getattr(libro, "autores", [])]
                c = counts_map.get(libro.id, {})
                item.ejemplares_count = int(c.get("total", 0))
                item.ejemplares_disponibles = int(c.get("disponible", 0))
                item.ejemplares_reservados = int(c.get("reservado", 0))
                item.ejemplares_prestados = int(c.get("prestado", 0))
                item.ejemplares_danados = int(c.get("danado", 0))
                items.append(item)
            return PaginatedResponse.create(items, total, pagination)

        # Sin paginación (comportamiento original)
        if normalizado:
            result = await db.execute(
                select(Libro).options(
                    selectinload(Libro.categoria),
                    selectinload(Libro.autores),
                    selectinload(Libro.ejemplar),
                )
            )
            libros = result.scalars().all()
            return [LibroViewNormalized.from_model(libro) for libro in libros]
        result = await db.execute(
            select(Libro).options(selectinload(Libro.autores))
        )
        libros = result.scalars().all()

        # obtener conteos de ejemplares por libro en una sola consulta
        libro_ids = [l.id for l in libros]
        if libro_ids:
            counts_stmt = (
                select(
                    Ejemplar.libro_id,
                    func.count(Ejemplar.id).label("total"),
                    func.sum(case((Ejemplar.estado_id == settings.DISPONIBILIDAD_EJEMPLAR_DISPONIBLE_ID, 1), else_=0)).label("disponible"),
                    func.sum(case((Ejemplar.estado_id == settings.RESERVADO_EJEMPLAR_ID, 1), else_=0)).label("reservado"),
                    func.sum(case((Ejemplar.estado_id == settings.PRESTADO_EJEMPLAR_NO_DISPONIBLE_ID, 1), else_=0)).label("prestado"),
                    func.sum(case((Ejemplar.estado_id == 6, 1), else_=0)).label("danado"),
                )
                .where(Ejemplar.libro_id.in_(libro_ids))
                .group_by(Ejemplar.libro_id)
            )
            counts_result = await db.execute(counts_stmt)
            counts_rows = counts_result.all()
            counts_map = {r.libro_id: r._asdict() for r in counts_rows}
        else:
            counts_map = {}

        items = []
        from ..schemas.autor_sch import AutorSimpleView
        for libro in libros:
            item = LibroView.model_validate(libro)
            item.autores = [AutorSimpleView.model_validate(a) for a in getattr(libro, "autores", [])]
            c = counts_map.get(libro.id, {})
            item.ejemplares_count = int(c.get("total", 0))
            item.ejemplares_disponibles = int(c.get("disponible", 0))
            item.ejemplares_reservados = int(c.get("reservado", 0))
            item.ejemplares_prestados = int(c.get("prestado", 0))
            item.ejemplares_danados = int(c.get("danado", 0))
            items.append(item)
        return items

    @staticmethod
    async def obtener_libro_por_id(
        libro_id: int, db: AsyncSession, normalizado: bool
    ) -> LibroView | LibroViewNormalized:
        """Obtener un libro por su ID."""
        if normalizado:
            result = await db.execute(
                select(Libro)
                .options(
                    selectinload(Libro.categoria),
                    selectinload(Libro.autores),
                )
                .where(Libro.id == libro_id)
            )
            libro = result.scalar()
            if not libro:
                raise HTTPException(status_code=404, detail="Libro no encontrado")
            # calcular counts sin cargar ejemplares
            counts_stmt = (
                select(
                    func.count(Ejemplar.id).label("total"),
                    func.sum(case((Ejemplar.estado_id == settings.DISPONIBILIDAD_EJEMPLAR_DISPONIBLE_ID, 1), else_=0)).label("disponible"),
                    func.sum(case((Ejemplar.estado_id == settings.RESERVADO_EJEMPLAR_ID, 1), else_=0)).label("reservado"),
                    func.sum(case((Ejemplar.estado_id == settings.PRESTADO_EJEMPLAR_NO_DISPONIBLE_ID, 1), else_=0)).label("prestado"),
                    func.sum(case((Ejemplar.estado_id == 6, 1), else_=0)).label("danado"),
                )
                .where(Ejemplar.libro_id == libro.id)
            )
            counts_result = await db.execute(counts_stmt)
            row = counts_result.first()
            item = LibroViewNormalized.from_model(libro)
            if row:
                item.ejemplares_count = int(row.total or 0)
                item.ejemplares_disponibles = int(row.disponible or 0)
                item.ejemplares_reservados = int(row.reservado or 0)
                item.ejemplares_prestados = int(row.prestado or 0)
                item.ejemplares_danados = int(row.danado or 0)
            return item
        result = await db.execute(
            select(Libro).options(selectinload(Libro.autores))
            .where(Libro.id == libro_id)
        )
        libro = result.scalar()
        if not libro:
            raise HTTPException(status_code=404, detail="Libro no encontrado")
        item = LibroView.model_validate(libro)
        from ..schemas.autor_sch import AutorSimpleView
        item.autores = [AutorSimpleView.model_validate(a) for a in getattr(libro, "autores", [])]

        # obtener conteos de ejemplares para este libro
        counts_stmt = select(
            func.count(Ejemplar.id).label("total"),
            func.sum(case((Ejemplar.estado_id == settings.DISPONIBILIDAD_EJEMPLAR_DISPONIBLE_ID, 1), else_=0)).label("disponible"),
            func.sum(case((Ejemplar.estado_id == settings.RESERVADO_EJEMPLAR_ID, 1), else_=0)).label("reservado"),
            func.sum(case((Ejemplar.estado_id == settings.PRESTADO_EJEMPLAR_NO_DISPONIBLE_ID, 1), else_=0)).label("prestado"),
            func.sum(case((Ejemplar.estado_id == 6, 1), else_=0)).label("danado"),
        ).where(Ejemplar.libro_id == libro.id)
        counts_result = await db.execute(counts_stmt)
        row = counts_result.first()
        if row:
            item.ejemplares_count = int(row.total or 0)
            item.ejemplares_disponibles = int(row.disponible or 0)
            item.ejemplares_reservados = int(row.reservado or 0)
            item.ejemplares_prestados = int(row.prestado or 0)
            item.ejemplares_danados = int(row.danado or 0)
        return item

    @staticmethod
    async def actualizar_libro(
        libro_id: int, libro_update: LibroUpdate, db: AsyncSession
    ) -> LibroView:
        """Actualizar un libro existente por su ID."""
        result = await db.execute(select(Libro).where(Libro.id == libro_id))
        libro = result.scalar_one_or_none()

        if not libro:
            raise HTTPException(status_code=404, detail="Libro no encontrado")

        update_data = libro_update.model_dump(exclude_unset=True)
        # manejar autores si vienen en la actualización
        autores_ids = update_data.pop("autores_ids", None)
        for var, value in update_data.items():
            setattr(libro, var, value)

        if autores_ids is not None:
            # reemplazar la lista de autores por la nueva
            result = await db.execute(select(Autor).where(Autor.id.in_(autores_ids)))
            autores = result.scalars().all()
            found_ids = {a.id for a in autores}
            missing = set(autores_ids) - found_ids
            if missing:
                raise HTTPException(status_code=400, detail=f"Autores no encontrados: {sorted(list(missing))}")
            libro.autores = autores

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
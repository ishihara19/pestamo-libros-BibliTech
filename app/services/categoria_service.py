from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException


from ..models.categoria import Categoria
from ..schemas.categoria_sch import CategoriaCreate, CategoriaUpdate, CategoriaView
from ..schemas.paginacion_sch import PaginationParams, PaginatedResponse
from ..schemas.generic_sch import GenericMessage


class CategoriaService:

    @staticmethod
    async def create_categoria(
        categoria: CategoriaCreate, db: AsyncSession
    ) -> CategoriaView:
        """Crear una nueva categoría en la base de datos."""
        nueva_categoria = Categoria(**categoria.model_dump())
        db.add(nueva_categoria)
        await db.commit()
        await db.refresh(nueva_categoria)
        return CategoriaView.model_validate(nueva_categoria)

    @staticmethod
    async def listar_categorias(
        db: AsyncSession, pagination: PaginationParams | None = None
    ) -> list[CategoriaView] | PaginatedResponse[CategoriaView]:
        """
        Listar todas las categorías en la base de datos.
        Si se proveen parámetros de paginación, retorna una respuesta paginada.
        """
        if pagination:
            # Contar total de registros
            count_query = select(func.count(Categoria.id))
            total_result = await db.execute(count_query)
            total = total_result.scalar()

            # Obtener registros paginados
            query = select(Categoria).offset(pagination.offset).limit(pagination.limit)
            result = await db.execute(query)
            categorias = result.scalars().all()

            items = [
                CategoriaView.model_validate(categoria) for categoria in categorias
            ]
            return PaginatedResponse.create(items, total, pagination)

        # Sin paginación (comportamiento original)
        result = await db.execute(select(Categoria))
        categorias = result.scalars().all()
        return [CategoriaView.model_validate(categoria) for categoria in categorias]

    @staticmethod
    async def obtener_categoria_por_id(
        categoria_id: int, db: AsyncSession
    ) -> CategoriaView:
        """Obtener una categoría por su ID."""
        result = await db.execute(select(Categoria).where(Categoria.id == categoria_id))
        categoria = result.scalar()
        if not categoria:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")
        return CategoriaView.model_validate(categoria)
    
    @staticmethod
    async def actualizar_categoria(
        categoria_id: int, 
        categoria_update: CategoriaUpdate, 
        db: AsyncSession
    ) -> CategoriaView:
        """Actualizar una categoría existente por su ID."""
        result = await db.execute(select(Categoria).where(Categoria.id == categoria_id))
        categoria = result.scalar_one_or_none()

        if not categoria:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")

        for var, value in categoria_update.model_dump(exclude_unset=True).items():
            setattr(categoria, var, value)

        db.add(categoria)
        await db.commit()
        await db.refresh(categoria)

        return CategoriaView.model_validate(categoria)

    @staticmethod
    async def eliminar_categoria(categoria_id: int, db: AsyncSession) -> GenericMessage:
        """Eliminar una categoría por su ID."""
        result = await db.execute(select(Categoria).where(Categoria.id == categoria_id))
        categoria = result.scalar_one_or_none()

        if not categoria:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")

        await db.delete(categoria)
        await db.commit()

        return GenericMessage(message="Categoría eliminada exitosamente")

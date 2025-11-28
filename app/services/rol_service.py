from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException

from ..schemas.paginacion_sch import PaginationParams, PaginatedResponse
from ..models.rol import Rol
from ..schemas.rol_sch import RolCreate, RolUpdate, RolView

class RolService:
    """Servicio para manejar operaciones relacionadas con el modelo Rol."""

    @staticmethod
    async def create_role(role: RolCreate, db: AsyncSession) -> RolView:
        """Crear un nuevo rol en la base de datos."""
        nuevo_rol = Rol(**role.model_dump())
        db.add(nuevo_rol)
        await db.commit()
        await db.refresh(nuevo_rol)
        return RolView.model_validate(nuevo_rol)

    @staticmethod
    async def listar_roles(
        db: AsyncSession, 
        pagination: PaginationParams | None = None
    ) -> list[RolView] | PaginatedResponse[RolView]:
        """
        Listar todos los roles en la base de datos.
        Si se proveen parámetros de paginación, retorna una respuesta paginada.
        """
        if pagination:
            # Contar total de registros
            count_query = select(func.count(Rol.id))
            total_result = await db.execute(count_query)
            total = total_result.scalar()
            
            # Obtener registros paginados
            query = (
                select(Rol)
                .offset(pagination.offset)
                .limit(pagination.limit)
            )
            result = await db.execute(query)
            roles = result.scalars().all()
            
            items = [RolView.model_validate(rol) for rol in roles]
            return PaginatedResponse.create(items, total, pagination)
        
        # Sin paginación (comportamiento original)
        result = await db.execute(select(Rol))
        roles = result.scalars().all()
        return [RolView.model_validate(rol) for rol in roles]
    
    @staticmethod
    async def obtener_role(id: int, db: AsyncSession) -> RolView | None:
        """Obtener un rol por su ID."""
        result = await db.execute(select(Rol).where(Rol.id == id))
        role = result.scalar()
        return RolView.model_validate(role) if role else None

    @staticmethod
    async def actualizar_role(id: int, role_update: RolUpdate, db: AsyncSession) -> RolView:
        """Actualizar un rol existente."""
        result = await db.execute(select(Rol).where(Rol.id == id))
        role = result.scalar()
        
        if not role:
            raise HTTPException(status_code=404, detail="Rol no encontrado")
        
        for var, value in role_update.model_dump(exclude_unset=True).items():
            setattr(role, var, value)
        
        db.add(role)
        await db.commit()
        await db.refresh(role)
        return RolView.model_validate(role)
    
    @staticmethod
    async def eliminar_role(id: int, db: AsyncSession) -> None:
        """Eliminar un rol por su ID."""
        result = await db.execute(select(Rol).where(Rol.id == id))
        role = result.scalar()
        
        if not role:
            raise HTTPException(status_code=404, detail="Rol no encontrado")

        await db.delete(role)
        await db.commit()
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import selectinload

from ..schemas.paginacion_sch import PaginationParams, PaginatedResponse
from ..models.usuario import Usuario
from ..schemas.usuario_sch import UsuarioCreate, UsuarioUpdatePerfil, UsuarioView, UsuarioUpdateContrasena, UsuarioResetearContrasena, UsuarioVerificarToken, UsuarioMensaje, UsuarioReadNormalized
from ..core.security import hash_password, verify_password
from ..utils.generar_token import generar_token
from ..utils.enviar_correo import enviar_correo_restablecimiento
from ..core.config import settings

class UsuarioService:
    
    @staticmethod
    async def create_usuario(usuario: UsuarioCreate, db: AsyncSession) -> UsuarioView:
        """Crear un nuevo usuario en la base de datos."""
        nuevo_usuario = Usuario(**usuario.model_dump())
        nuevo_usuario.contrasena = hash_password(usuario.contrasena)
        db.add(nuevo_usuario)
        await db.commit()
        await db.refresh(nuevo_usuario)
        return UsuarioView.model_validate(nuevo_usuario)

    @staticmethod
    async def listar_usuarios(
        db: AsyncSession, 
        pagination: PaginationParams | None = None,
        normalizado: bool = False
    ) -> list[UsuarioView] | PaginatedResponse[UsuarioView]:
        """
        Listar todos los usuarios en la base de datos.
        Si se proveen parámetros de paginación, retorna una respuesta paginada.
        """
        if pagination:
            # Contar total de registros
            count_query = select(func.count(Usuario.id))
            total_result = await db.execute(count_query)
            total = total_result.scalar()
            
            if normalizado:
                # Obtener registros paginados
                query = (
                    select(Usuario).options(
                selectinload(Usuario.rol),
                selectinload(Usuario.estado),
                selectinload(Usuario.tipo_documento),)
                    .offset(pagination.offset)
                    .limit(pagination.limit)
                    )                
        
                result = await db.execute(query)
                usuarios = result.scalars().all()
            
                items = [UsuarioReadNormalized.from_model(usuario) for usuario in usuarios]
                return PaginatedResponse.create(items, total, pagination)
                
            query = (
                select(Usuario)
                .offset(pagination.offset)
                .limit(pagination.limit)
            ) 
            result = await db.execute(query)
            usuarios = result.scalars().all()   
            items = [UsuarioView.model_validate(usuario) for usuario in usuarios]
            return PaginatedResponse.create(items, total, pagination)
        
        # Sin paginación (comportamiento original)
        if normalizado:
            result = await db.execute(select(Usuario).options(
                selectinload(Usuario.rol),
                selectinload(Usuario.estado),
                selectinload(Usuario.tipo_documento),)
            )
            usuarios = result.scalars().all()
            return [UsuarioReadNormalized.from_model(usuario) for usuario in usuarios]
        result = await db.execute(select(Usuario))
        usuarios = result.scalars().all()
        return [UsuarioView.model_validate(usuario) for usuario in usuarios]

    @staticmethod
    async def obtener_usuario(id: int, db: AsyncSession) -> UsuarioView | None:
        """Obtener un usuario por su ID."""
        result = await db.execute(select(Usuario).where(Usuario.id == id))
        usuario = result.scalar()
        return UsuarioView.model_validate(usuario) if usuario else None

    @staticmethod
    async def actualizar_perfil_usuario(
        id: int, 
        usuario_update: UsuarioUpdatePerfil, 
        db: AsyncSession
    ) -> UsuarioView:
        """Actualizar el perfil de un usuario."""
        result = await db.execute(select(Usuario).where(Usuario.id == id))
        usuario = result.scalar()
        
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        for var, value in usuario_update.model_dump(exclude_unset=True).items():
            setattr(usuario, var, value)
        
        db.add(usuario)
        await db.commit()
        await db.refresh(usuario)
        
        return UsuarioView.model_validate(usuario)

    @staticmethod
    async def actualizar_contrasena_usuario(
        id: int, 
        usuario_update: UsuarioUpdateContrasena, 
        db: AsyncSession
    ) -> UsuarioMensaje:
        """Actualizar la contraseña de un usuario."""
        result = await db.execute(select(Usuario).where(Usuario.id == id))
        usuario = result.scalar()
        
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        if not verify_password(usuario_update.contrasena_actual, usuario.contrasena):
            raise HTTPException(status_code=400, detail="Contraseña actual incorrecta")
        
        usuario.contrasena = hash_password(usuario_update.contrasena_nueva)
        
        db.add(usuario)
        await db.commit()
        return UsuarioMensaje(message="Contraseña actualizada exitosamente")

    @staticmethod
    async def restablecer_contrasena_usuario(contrasena_resetear: UsuarioResetearContrasena, db: AsyncSession) -> None:
        """Restablecer la contraseña de un usuario."""
        result = await db.execute(select(Usuario).where(Usuario.correo == contrasena_resetear.correo))
        usuario = result.scalar()
        
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        token = generar_token()
        usuario.token = token 
        usuario.token_expiracion = datetime.now(timezone.utc) + timedelta(minutes=settings.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES)
        await db.commit()
        
        await enviar_correo_restablecimiento(usuario.correo, token)
        
        return UsuarioMensaje(message="Correo de restablecimiento enviado")

    @staticmethod
    async def verificar_token_usuario(verificacion: UsuarioVerificarToken, db: AsyncSession) -> UsuarioMensaje:
        """Verificar el token de restablecimiento de contraseña."""
        result = await db.execute(select(Usuario).where(Usuario.correo == verificacion.correo))
        usuario = result.scalar()
        
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        if usuario.token != verificacion.token:
            raise HTTPException(status_code=400, detail="Token inválido")
        
        if not usuario.token_expiracion or usuario.token_expiracion < datetime.now(timezone.utc):
            raise HTTPException(status_code=400, detail="Token expirado")
        
        usuario.contrasena = hash_password(verificacion.contrasena_nueva)
        usuario.token = None 
        usuario.token_expiracion = None
        db.add(usuario)
        await db.commit()
        
        return UsuarioMensaje(message="Contraseña restablecida exitosamente")

    @staticmethod
    async def eliminar_usuario(id: int, db: AsyncSession) -> UsuarioMensaje:
        """Eliminar un usuario por su ID."""
        result = await db.execute(select(Usuario).where(Usuario.id == id))
        usuario = result.scalar()
        
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        await db.delete(usuario)
        await db.commit()
        
        return UsuarioMensaje(message="Usuario eliminado exitosamente")
        
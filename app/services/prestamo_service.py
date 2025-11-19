from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update
from fastapi import HTTPException
from datetime import datetime, timedelta, timezone, date
from sqlalchemy.orm import selectinload
from typing import Optional


from ..models.prestamo import Prestamo
from ..models.usuario import Usuario
from ..models.ejemplar import Ejemplar
from ..core.db.postgre import set_app_context, clear_app_context
from ..utils.utils import generar_fecha_devolucion_prevista, ejemplar_disponible_info
from ..schemas.paginacion_sch import PaginationParams, PaginatedResponse
from ..schemas.prestamo_sch import HacerPrestamo, PrestamoViewBibliotecario, PrestamoViewNormalizedBibliotecario, PrestamoViewNormalizedLector, ConfirmarEntregaPrestamo
from ..schemas.generic_sch import GenericMessage
from ..core.config import settings


class PrestamoService:
    @staticmethod
    async def crear_prestamo(
        db: AsyncSession,
        prestamo_data: HacerPrestamo,
        usuario_id: int,
        ip: str,
        host: str,
        username: str,
    ) -> GenericMessage:
        """Crear un nuevo préstamo"""
        try:
            # Establecer contexto de la aplicación
            await set_app_context(db, username, ip, host, "crear_prestamo")
            # Generar fecha prevista de devolución
            fecha_prevista_devolucion = await generar_fecha_devolucion_prevista(
                prestamo_data.fecha_solicitud.date(), prestamo_data.dias_prestamo
            )
            # Verificar disponibilidad del ejemplar
            ejemplar = await ejemplar_disponible_info(prestamo_data.libro_id, db)

            if ejemplar is None:
                raise HTTPException(
                    status_code=400,
                    detail="No hay ejemplares disponibles para el libro solicitado.",
                )
            # Crear el préstamo
            nuevo_prestamo = Prestamo(
                usuario_id=usuario_id,
                ejemplar_id=ejemplar["id"],
                fecha_solicitud=prestamo_data.fecha_solicitud,
                fecha_prevista_devolucion=fecha_prevista_devolucion,
            )
            # Guardar en la base de datos
            db.add(nuevo_prestamo)
            # Cambiar el estado del ejemplar a 'Reservado'
            stmt = (
                update(Ejemplar)
                .where(Ejemplar.id == ejemplar["id"])
                .values(estado_id=settings.RESERVADO_EJEMPLAR_ID)
            )
            # Ejecutar las operaciones
            await db.execute(stmt)
            # Confirmar los cambios
            await db.commit()

            return GenericMessage(
                message=f"Préstamo creado exitosamente con el ejemplar {ejemplar['codigo_interno']}."
            )

        except Exception as e:
            
            await db.rollback()
            raise

        finally:

            await clear_app_context(db)


    async def listar_prestamos_bibliotecario(
        db: AsyncSession,
        pagination: PaginationParams | None = None,
        normalizado: bool = False,
    ) ->(
        list[PrestamoViewBibliotecario]
        | list[PrestamoViewNormalizedBibliotecario]
        | PaginatedResponse[PrestamoViewBibliotecario]
        | PaginatedResponse[PrestamoViewNormalizedBibliotecario]
    ):
        """Listar todos los préstamos realizados."""
        if pagination:
            # Contar total de registros
            count_query = select(func.count(Prestamo.id))
            total_result = await db.execute(count_query)
            total = total_result.scalar()
            if normalizado:
                # Obtener registros paginados
                query = (
                    select(Prestamo)
                    .options(
                        selectinload(Prestamo.usuarios),
                        selectinload(Prestamo.ejemplar).selectinload(Ejemplar.libro),
                        selectinload(Prestamo.ejemplar).selectinload(Ejemplar.estado),
                    )
                    .offset(pagination.offset)
                    .limit(pagination.limit)
                )
                result = await db.execute(query)
                prestamos = result.scalars().all()

                items = [
                    PrestamoViewNormalizedBibliotecario.from_model(prestamo)
                    for prestamo in prestamos
                ]
                return PaginatedResponse.create(items, total, pagination)
            # Obtener registros paginados
            query = (
                select(Prestamo)
                .offset(pagination.offset)
                .limit(pagination.limit)
            )
            result = await db.execute(query)
            prestamos = result.scalars().all()

            items = [PrestamoViewBibliotecario.model_validate(prestamo) for prestamo in prestamos]
            return PaginatedResponse.create(items, total, pagination)

        if normalizado:
            # Obtener todos los registros
            query = select(Prestamo).options(
                selectinload(Prestamo.usuarios),
                selectinload(Prestamo.ejemplar).selectinload(Ejemplar.libro),
                selectinload(Prestamo.ejemplar).selectinload(Ejemplar.estado),
            )
            result = await db.execute(query)
            prestamos = result.scalars().all()

            return [
                PrestamoViewNormalizedBibliotecario.from_model(prestamo)
                for prestamo in prestamos
            ]
        # Obtener todos los registros
        query = select(Prestamo)
        result = await db.execute(query)
        prestamos = result.scalars().all()

        return [PrestamoViewBibliotecario.model_validate(prestamo) for prestamo in prestamos]

    @staticmethod
    async def listar_prestamos_lector(
        db: AsyncSession,
        usuario_id: int,
        pagination: PaginationParams | None = None,        
    ) -> list[PrestamoViewNormalizedLector]:

        if pagination:
            # Contar total
            count_query = select(func.count(Prestamo.id)).where(Prestamo.usuario_id == usuario_id)
            total_result = await db.execute(count_query)
            total = total_result.scalar()

            # Consulta con relaciones cargadas
            query = (
                select(Prestamo)
                .where(Prestamo.usuario_id == usuario_id)
                .options(
                    selectinload(Prestamo.ejemplar).selectinload(Ejemplar.libro),
                    selectinload(Prestamo.ejemplar).selectinload(Ejemplar.estado),
                )
                .offset(pagination.offset)
                .limit(pagination.limit)
            )

            result = await db.execute(query)
            prestamos = result.scalars().all()

            items = [
                PrestamoViewNormalizedLector.from_model(prestamo)
                for prestamo in prestamos
            ]
            return PaginatedResponse.create(items, total, pagination)
     
        query = (
            select(Prestamo)
            .where(Prestamo.usuario_id == usuario_id)
            .options(
                selectinload(Prestamo.ejemplar).selectinload(Ejemplar.libro),
                selectinload(Prestamo.ejemplar).selectinload(Ejemplar.estado),
            )
        )

        result = await db.execute(query)
        prestamos = result.scalars().all()

        return [
            PrestamoViewNormalizedLector.from_model(prestamo)
            for prestamo in prestamos
        ]

    @staticmethod
    async def confirmar_entrega_por_documento(
        db: AsyncSession,
        datos_prestamo: ConfirmarEntregaPrestamo,
        ip: str,
        host: str,
        username: str,    
    ) -> GenericMessage:
        """Confirmar la entrega de un préstamo por número de documento y código interno del ejemplar"""
        try:
            await set_app_context(db, username, ip, host, "confirmar_entrega_por_documento")
            # Buscar el préstamo correspondiente
            query = (
                select(Prestamo)
                .options(selectinload(Prestamo.ejemplar))
                .join(Prestamo.usuarios)
                .join(Prestamo.ejemplar)
                .where(
                    Usuario.documento == datos_prestamo.numero_documento,
                    Ejemplar.codigo_interno == datos_prestamo.ejemplar_codigo_interno,
                    Ejemplar.estado_id == settings.RESERVADO_EJEMPLAR_ID
                )
            )
            
            # Ejecutar la consulta
            result = await db.execute(query)
            prestamo = result.scalar_one_or_none()
            
            # Validar existencia del préstamo
            if not prestamo:
                return GenericMessage(message="No existe un préstamo reservado para este usuario y ejemplar.")

            # Actualizar el préstamo y el estado del ejemplar
            prestamo.fecha_entrega = date.today()       
            prestamo.ejemplar.estado_id = settings.PRESTADO_EJEMPLAR_NO_DISPONIBLE_ID
    
            
            await db.commit()
            await db.refresh(prestamo)

            return GenericMessage(message="Entrega confirmada. El ejemplar fue marcado como prestado.")
        
        except Exception as e:            
            await db.rollback()
            raise

        finally:

            await clear_app_context(db)    
            
            
    @staticmethod
    async def registrar_devolucion(
        db: AsyncSession,
        codigo_interno: str,
        ip: str,
        host: str,
        username: str,
    ) -> GenericMessage:

        try:
            await set_app_context(db, username, ip, host, "registrar_devolucion")

            # Buscar el préstamo activo por código interno
            query = (
                select(Prestamo)
                .options(
                    selectinload(Prestamo.ejemplar),  
                    selectinload(Prestamo.usuarios)
                )
                .join(Prestamo.ejemplar)
                .where(
                    Ejemplar.codigo_interno == codigo_interno,
                    Prestamo.fecha_devuelto.is_(None),  # préstamo aún activo
                    Ejemplar.estado_id == settings.PRESTADO_EJEMPLAR_NO_DISPONIBLE_ID
                )
            )

            result = await db.execute(query)
            prestamo = result.scalar_one_or_none()

            if not prestamo:
                return GenericMessage(message="No existe un préstamo activo para este ejemplar.")

            # Cambiar estados
            prestamo.fecha_devuelto = datetime.now()
            prestamo.ejemplar.estado_id = settings.DISPONIBILIDAD_EJEMPLAR_DISPONIBLE_ID

            await db.commit()
            await db.refresh(prestamo)

            return GenericMessage(message="Devolución registrada correctamente.")
        
        except Exception as e:
            await db.rollback()
            raise

        finally:
            await clear_app_context(db)
            

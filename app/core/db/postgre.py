from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import text
from ..config import settings
from typing import AsyncGenerator

# --- Engine con pool_pre_ping para reconectar automáticamente ---
engine = create_async_engine(
    settings.POSTGRES_URL, echo=False, pool_pre_ping=True, future=True
)

# --- Sessionmaker ---
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# --- Base para modelos ---
Base = declarative_base()


# --- Crear tablas al iniciar la app ---
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Tablas creadas/verificadas en PostgreSQL")


# --- Dependency para FastAPI ---
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def set_app_context(
    db: AsyncSession, usuario_app: str, ip: str, host: str, operacion: str
):
    # Escapamos comillas simples para evitar errores de sintaxis
    def safe(value: str) -> str:
        return value.replace("'", "''") if value else ""

    await db.execute(text(f"SET LOCAL \"app.usuario_app\" = '{safe(usuario_app)}'"))
    await db.execute(text(f"SET LOCAL \"app.ip\" = '{safe(ip)}'"))
    await db.execute(text(f"SET LOCAL \"app.host\" = '{safe(host)}'"))
    await db.execute(text(f"SET LOCAL \"app.operation\" = '{safe(operacion)}'"))


async def clear_app_context(db: AsyncSession):
    await db.execute(text('RESET "app.usuario_app"'))
    await db.execute(text('RESET "app.ip"'))
    await db.execute(text('RESET "app.host"'))
    await db.execute(text('RESET "app.operation"'))

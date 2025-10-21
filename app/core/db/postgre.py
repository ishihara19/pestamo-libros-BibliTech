from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from ..config import settings
from typing import AsyncGenerator

# --- Engine con pool_pre_ping para reconectar automáticamente ---
engine = create_async_engine(
    settings.POSTGRES_URL,
    echo=False,
    pool_pre_ping=True,  
    future=True
)

# --- Sessionmaker ---
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

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
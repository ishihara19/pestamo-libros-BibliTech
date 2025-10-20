from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from ..config import settings
from typing import AsyncGenerator

engine = create_async_engine(settings.POSTGRES_URL, echo=False)

async_session = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

async def on_startup():
        async with engine.begin() as conn:
            # Esto crea las tablas si no existen
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Tablas creadas/verificadas en PostgreSQL")

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session     
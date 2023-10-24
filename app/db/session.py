from typing import Generator

from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.settings import settings

engine: AsyncEngine = create_async_engine(settings.database_url, echo=True)

Session: AsyncSession = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
    bind=engine
)


async def get_session() -> Generator:
    """Retorna uma sessão do banco de dados"""
    session: AsyncSession = Session()

    try:
        yield session
    finally:
        await session.close()

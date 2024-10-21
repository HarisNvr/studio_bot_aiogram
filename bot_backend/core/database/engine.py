from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from core.middleware.settings import DATABASE_URL, ENGINE_ECHO

engine = create_async_engine(
    DATABASE_URL,
    echo=ENGINE_ECHO
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Return session generator instance to interact with the database."""

    async with AsyncSessionLocal() as async_session:
        yield async_session

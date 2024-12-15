from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from core.components.settings import DATABASE_URL, ENGINE_ECHO

engine = create_async_engine(
    url=DATABASE_URL,
    echo=ENGINE_ECHO
)

async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

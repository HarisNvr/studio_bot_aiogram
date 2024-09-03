from sqlalchemy.ext.asyncio import (
    AsyncSession, create_async_engine, async_sessionmaker
)

from bot_backend.core.middleware.settings import DATABASE_URL, ENGINE_ECHO

engine = create_async_engine(
    DATABASE_URL,
    echo=ENGINE_ECHO
)
"""Create an asynchronous engine for interacting with the database."""

session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)
"""
Create a session maker for generating asynchronous sessions with the database.
"""


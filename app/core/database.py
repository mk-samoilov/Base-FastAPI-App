"""
Database configuration and session management.
"""

from typing import Annotated, AsyncGenerator
from fastapi import Depends

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from sqlalchemy.orm import DeclarativeBase

from app.config import settings


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass


engine: AsyncEngine | None = None
session_factory: async_sessionmaker[AsyncSession] | None = None


def init_database(database_url: str | None = None) -> None:
    """
    Initialize database engine and session factory.

    Args:
        database_url: Database connection URL (defaults to settings.database_url)
    """

    global engine, session_factory

    if database_url is None:
        database_url = settings.database_url

    engine = create_async_engine(database_url, echo=False)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)


async def create_tables() -> None:
    """Create all tables from registered models."""

    if engine is None:
        raise RuntimeError("Database not initialized")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables() -> None:
    """Drop all tables."""

    if engine is None:
        raise RuntimeError("Database not initialized")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting database session."""

    if session_factory is None:
        raise RuntimeError("Database not initialized")

    async with session_factory() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    """Get session factory for service initialization."""

    if session_factory is None:
        raise RuntimeError("Database not initialized")

    return session_factory

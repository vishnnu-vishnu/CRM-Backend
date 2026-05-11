# app/db/session.py

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


# Detect SQLite
_is_sqlite = settings.DATABASE_URL.startswith("sqlite")


# Engine Configuration
_engine_kwargs: dict = {
    "echo": settings.DEBUG,
}

# SQLite configuration
if _is_sqlite:
    _engine_kwargs["connect_args"] = {
        "check_same_thread": False
    }

# PostgreSQL / MySQL configuration
else:
    _engine_kwargs.update(
        {
            "pool_pre_ping": True,
            "pool_size": 10,
            "max_overflow": 20,
            "pool_recycle": 3600,
        }
    )


# Create Async Engine
engine = create_async_engine(
    settings.DATABASE_URL,
    **_engine_kwargs,
)


# Session Factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


# Base Model
class Base(DeclarativeBase):
    pass


# Dependency
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()

        except Exception:
            await session.rollback()
            raise

        finally:
            await session.close()


# Initialize Database
async def init_db():
    """
    Create all database tables.
    Use only for development.
    Use Alembic migrations in production.
    """

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
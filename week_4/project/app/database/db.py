from collections.abc import AsyncGenerator

from app.core.settings import settings
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=settings.DEBUG,
)


SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy ORM models.
    """


async def get_db() -> AsyncGenerator[AsyncSession]:
    """
    FastAPI dependency that yields an AsyncSession and rolls back
    on unhandled errors. The session is closed automatically by the
    async context manager on exit.
    """
    async with SessionLocal() as db:
        try:
            yield db
        except Exception:
            await db.rollback()
            raise

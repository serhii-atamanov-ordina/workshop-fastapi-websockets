"""Set up the database connection."""
import logging
from typing import Generator

from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from src.core.config import get_settings

logger = logging.getLogger(get_settings().LOGGER_CONTROLLERS_NAME)


engine = create_async_engine(
    "sqlite+aiosqlite:///test.db",
    future=True,
    echo=False,
    connect_args={"check_same_thread": False},
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
    future=True,
)
DeclarativeBase = declarative_base()


async def get_database() -> Generator[AsyncSession, None, None]:
    """Get a database session. Session is closed upon exiting the generator.

    Returns:
        Generator containing the database session.

    """
    logger.debug("starting database session")
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        logger.debug("closing database session")
        await db.close()

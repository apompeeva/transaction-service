from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

DATABASE_URL_SYNC = f'postgresql+psycopg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'  # noqa: E501


class Base(DeclarativeBase):
    """Base class used for declarative class definitions."""

    pass


sync_engine = create_engine(url=DATABASE_URL_SYNC)

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine)

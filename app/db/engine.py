import os

from contextlib import asynccontextmanager
from typing import Any, AsyncIterator
from dotenv import load_dotenv, find_dotenv

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

load_dotenv(find_dotenv())


DATABASE_URL: str = (
    f"postgresql+asyncpg://"
    f"{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/"
    f"{os.getenv('POSTGRES_DB')}"
)


class Base(DeclarativeBase):
    __mapper_args__ = {"eager_defaults": True}
    
    
class DBSessionManager:
    def __init__(self, host: str, engine_kwargs: dict[str, Any] = {}):
        self._engine = create_async_engine(host, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine)

    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


sessionmanager = DBSessionManager(DATABASE_URL, {"echo": False})


class DatabaseMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: TelegramObject, data: dict):
        async with sessionmanager.session() as session:
            data["db_session"] = session
            return await handler(event, data)
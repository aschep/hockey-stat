import os
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from sqlalchemy import NullPool, event
from sqlalchemy.ext import asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker

from .dao.team import TeamDAO
from .dao.tournament import GroupDAO, TournamentDAO

DATABASE_URL = f"sqlite+aiosqlite:///{os.getenv('DATABASE_URL', 'hockeybot.db')}"

engine = asyncio.create_async_engine(DATABASE_URL, echo=False, poolclass=NullPool)
SessionLocal = asyncio.async_sessionmaker(engine, expire_on_commit=False)


@event.listens_for(engine.sync_engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA synchronous=NORMAL")
    cursor.execute("PRAGMA busy_timeout=20000")
    cursor.close()


# async def get_db() -> asyncio.AsyncSession:
#     async with SessionLocal() as session:
#         yield session


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        self.session_pool = session_pool

    async def __call__(
        self,
        handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: Dict[str, Any],
    ) -> Any:
        async with self.session_pool() as session:
            data["team_dao"] = TeamDAO(session)
            data["tour_dao"] = TournamentDAO(session)
            data["group_dao"] = GroupDAO(session)
            return await handler(event, data)

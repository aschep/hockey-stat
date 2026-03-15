import os
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from sqlalchemy.ext import asyncio

from .dao.team import TeamDAO

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///hockeybot.db")

engine = asyncio.create_async_engine(DATABASE_URL, echo=True)
SessionLocal = asyncio.async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> asyncio.AsyncSession:
    async with SessionLocal() as session:
        yield session


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, session: asyncio.AsyncSession):
        self.session = session

    async def __call__(
        self,
        handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: Dict[str, Any],
    ) -> Any:
        data["team_dao"] = TeamDAO(self.session)
        return await handler(event, data)

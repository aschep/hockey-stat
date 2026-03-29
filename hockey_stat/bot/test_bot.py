import asyncio
import logging
import os
from unittest.mock import AsyncMock, patch

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TEST
from aiogram.enums import ChatType, ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Chat, Message, Update
from dotenv import load_dotenv

from hockey_stat.bot import handlers
from hockey_stat.storage.middleware import DatabaseMiddleware, SessionLocal

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")


async def main():
    session = AiohttpSession(api=TEST)
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN), session=session)
    dp = Dispatcher(storage=MemoryStorage())

    async with SessionLocal() as db_session:
        dp.update.middleware(DatabaseMiddleware(db_session))
        dp.include_router(handlers.router)
        logger.info("Bot running")

        message = Message(
            message_id=1, date=12345678, chat=Chat(id=123, type=ChatType.PRIVATE), text="/groups ПФО 25/26 2013"
        )

        with patch.object(Message, "answer", new_callable=AsyncMock) as mock_answer:
            await dp.feed_update(bot, Update(update_id=123, message=message))

    logger.info("That's all!")


if __name__ == "__main__":
    asyncio.run(main())

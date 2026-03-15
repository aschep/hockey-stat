import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from hockey_stat.storage.middleware import DatabaseMiddleware, SessionLocal

from . import handlers

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    async with SessionLocal() as db_session:
        dp.update.middleware(DatabaseMiddleware(db_session))
        dp.include_router(handlers.router)
        logger.info("Bot running")
        await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

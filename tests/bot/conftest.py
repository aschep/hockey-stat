import pytest
from aiogram.enums import ChatType
from aiogram.types import Chat, Message, User

from hockey_stat.storage.middleware import SessionLocal


@pytest.fixture(scope="function")
async def get_async_db():
    async with SessionLocal() as session:
        yield session


@pytest.fixture
def mock_message():
    def create_message(text: str, chat_id: int = 123):
        return Message(
            message_id=100,
            date=1234567890,
            from_user=User(id=123, is_bot=False, first_name="test_user"),
            chat=Chat(id=chat_id, type=ChatType.PRIVATE),
            text=text,
        )

    return create_message

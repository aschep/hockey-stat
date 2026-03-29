from unittest.mock import AsyncMock, patch

import pytest
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    ReplyKeyboardRemove,
)

from hockey_stat.bot.handlers import (
    TournamentState,
    cmd_start,
    cmd_tours,
    make_row_keyboard,
)
from hockey_stat.storage.dao.tournament import TournamentDAO


class TestMakeKeyboard:
    def test_make_row_keyboard(self):
        """Проверяет создание клавиатуры с кнопками в один ряд."""
        items = ["Кнопка 1", "Кнопка 2", "Кнопка 3"]
        keyboard = make_row_keyboard(items, show_back=False, show_reset=False)

        assert isinstance(keyboard, InlineKeyboardMarkup)
        assert len(keyboard.inline_keyboard) == 1
        assert len(keyboard.inline_keyboard[0]) == 3

        row_buttons = keyboard.inline_keyboard[0]
        assert isinstance(row_buttons[0], InlineKeyboardButton)
        assert row_buttons[0].text == "Кнопка 1"
        assert row_buttons[1].text == "Кнопка 2"
        assert row_buttons[2].text == "Кнопка 3"

    def test_make_row_keyboard_empty(self):
        """Проверяет поведение на пустом списке."""
        keyboard = make_row_keyboard([], show_back=False, show_reset=False)

        assert isinstance(keyboard, InlineKeyboardMarkup)
        assert len(keyboard.inline_keyboard) == 0

    def test_make_row_keyboard_single_item(self):
        """Проверяет клавиатуру с одной кнопкой."""
        items = ["Единая"]
        keyboard = make_row_keyboard(items, show_back=False, show_reset=False)

        assert len(keyboard.inline_keyboard[0]) == 1
        assert keyboard.inline_keyboard[0][0].text == "Единая"


class TestBotHandlers:

    @pytest.mark.asyncio
    @patch.object(Message, "answer", new_callable=AsyncMock)
    async def test_start(self, mock_answer, mock_message):
        message = mock_message("/start")

        await cmd_start(
            message, FSMContext(storage=MemoryStorage(), key=StorageKey(chat_id=123, bot_id=10, user_id=1010))
        )

        mock_answer.assert_called_once_with(
            "Bot запущен!\n" "/tour - информация о текущем турнире",
            reply_markup=ReplyKeyboardRemove(remove_keyboard=True, selective=None),
        )

    @pytest.mark.asyncio
    @patch.object(Message, "answer", new_callable=AsyncMock)
    async def test_tournaments(self, mock_answer, mock_message, get_async_db):
        message = mock_message("/tours")

        await cmd_tours(message, TournamentDAO(get_async_db))

        mock_answer.assert_called_once_with("Турниры:\n\n")

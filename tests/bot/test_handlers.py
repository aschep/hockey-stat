from unittest.mock import AsyncMock, patch

import pytest
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup

from hockey_stat.bot.handlers import cmd_start, cmd_tours, make_row_keyboard
from hockey_stat.storage.dao.tournament import TournamentDAO


class TestMakeKeyboard:
    def test_make_row_keyboard(self):
        """Проверяет создание клавиатуры с кнопками в один ряд."""
        items = ["Кнопка 1", "Кнопка 2", "Кнопка 3"]
        keyboard = make_row_keyboard(items)

        assert isinstance(keyboard, ReplyKeyboardMarkup)
        assert len(keyboard.keyboard) == 1
        assert len(keyboard.keyboard[0]) == 3

        row_buttons = keyboard.keyboard[0]
        assert isinstance(row_buttons[0], KeyboardButton)
        assert row_buttons[0].text == "Кнопка 1"
        assert row_buttons[1].text == "Кнопка 2"
        assert row_buttons[2].text == "Кнопка 3"
        assert keyboard.resize_keyboard is True

    def test_make_row_keyboard_empty(self):
        """Проверяет поведение на пустом списке."""
        keyboard = make_row_keyboard([])

        assert isinstance(keyboard, ReplyKeyboardMarkup)
        assert len(keyboard.keyboard) == 1
        assert len(keyboard.keyboard[0]) == 0
        assert keyboard.resize_keyboard is True

    def test_make_row_keyboard_single_item(self):
        """Проверяет клавиатуру с одной кнопкой."""
        items = ["Единая"]
        keyboard = make_row_keyboard(items)

        assert len(keyboard.keyboard[0]) == 1
        assert keyboard.keyboard[0][0].text == "Единая"


class TestBotHandlers:

    @pytest.mark.asyncio
    @patch.object(Message, "answer", new_callable=AsyncMock)
    async def test_start(self, mock_answer, mock_message):
        message = mock_message("/start")

        await cmd_start(message)

        mock_answer.assert_called_once_with("Bot запущен!")

    @pytest.mark.asyncio
    @patch.object(Message, "answer", new_callable=AsyncMock)
    async def test_tournaments(self, mock_answer, mock_message, get_async_db):
        message = mock_message("/tours")

        await cmd_tours(message, TournamentDAO(get_async_db))

        mock_answer.assert_called_once_with("Турниры:\n\n")

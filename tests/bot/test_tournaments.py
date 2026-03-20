from unittest.mock import AsyncMock, patch

import pytest
from aiogram.types import Message

from hockey_stat.bot.handlers import cmd_start, cmd_tour
from hockey_stat.storage.dao.tournament import TournamentDAO


class TestBotHandlers:

    @pytest.mark.asyncio
    @patch.object(Message, "answer", new_callable=AsyncMock)
    async def test_start(self, mock_answer, mock_message):
        message = mock_message("/start")

        await cmd_start(message)

        mock_answer.assert_called_once_with("ХоккейStat Bot запущен!", parse_mode="Markdown")

    @pytest.mark.asyncio
    @patch.object(Message, "answer", new_callable=AsyncMock)
    async def test_tournaments(self, mock_answer, mock_message, get_async_db):
        message = mock_message("/tours")

        await cmd_tour(message, TournamentDAO(get_async_db))

        mock_answer.assert_called_once_with("Турниры:\n\n", parse_mode="Markdown")

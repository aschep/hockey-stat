from unittest.mock import AsyncMock, MagicMock

import pytest
from aiogram.types import Message

from hockey_stat.storage.dao.team import TeamDAO
from hockey_stat.storage.dao.tournament import GroupDAO, TournamentDAO
from hockey_stat.storage.middleware import DatabaseMiddleware


@pytest.mark.asyncio
async def test_database_middleware():
    middleware = DatabaseMiddleware(AsyncMock)

    async def mock_handler(event: Message, data: dict):
        assert "team_dao" in data
        assert "tour_dao" in data
        assert isinstance(data["team_dao"], TeamDAO)
        assert isinstance(data["tour_dao"], TournamentDAO)
        assert isinstance(data["group_dao"], GroupDAO)
        return "ok"

    event = MagicMock(spec=Message)
    data = {}

    result = await middleware(mock_handler, event, data)

    assert result == "ok"
    assert "team_dao" in data
    assert "tour_dao" in data
    assert "group_dao" in data

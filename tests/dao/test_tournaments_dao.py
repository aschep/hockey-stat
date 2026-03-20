import pytest
from sqlalchemy import text

from hockey_stat.storage.dao.tournament import TournamentDAO
from hockey_stat.storage.repository import TournamentRepository


@pytest.fixture
def create_env(get_db, tournament_db):
    try:
        get_db.commit()
        yield
    finally:
        get_db.execute(text("delete from tournaments;"))
        get_db.commit()


class TestTournamentsDao:

    @staticmethod
    def check_tournament(result, expected):
        assert result.name == expected.name
        assert result.age == expected.age
        assert result.url == expected.url
        assert result.key == expected.key

    @pytest.mark.asyncio
    async def test_tournaments_all(self, get_async_db, create_env, tournament):
        tours = await TournamentDAO(get_async_db).get_all()

        assert len(tours) == 1
        self.check_tournament(tours[0], tournament)

    async def test_tournaments_empty_list(self, get_async_db):
        tours = await TournamentDAO(get_async_db).get_all()

        assert len(tours) == 0

    @pytest.mark.asyncio
    async def test_tournaments_get(self, get_async_db, create_env, tournament):
        tour = await TournamentDAO(get_async_db).get(tournament.name, tournament.age)

        self.check_tournament(tour, tournament)

    @pytest.mark.asyncio
    async def test_tournaments_get_none(self, get_async_db, create_env):
        tour = await TournamentDAO(get_async_db).get("none tour", 123)

        assert not tour

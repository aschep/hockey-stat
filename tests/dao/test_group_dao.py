import pytest
from sqlalchemy import text

from hockey_stat.storage.dao.tournament import GroupDAO


@pytest.fixture
def create_env(get_db, tournament_db, group_db, group_team_stats_db, game_db):
    try:
        get_db.commit()
        yield
    finally:
        get_db.execute(text("delete from tournaments;"))
        get_db.commit()


class TestGroupDao:
    @pytest.mark.asyncio
    async def test_tournaments_get_groups(self, get_async_db, create_env, group_db):
        groups = await GroupDAO(get_async_db).get_group_names(group_db.tournament_id)

        assert len(groups) == 1
        assert groups[0] == group_db.name

    @pytest.mark.asyncio
    async def test_tournaments_get_group_table(self, get_async_db, create_env, group_db, group_team_stats_db):
        teams = await GroupDAO(get_async_db).get_group_table(group_db.name, group_db.tournament_id)

        assert len(teams) == 1
        team_stats = teams[0]
        assert team_stats.id == group_team_stats_db.id
        assert team_stats.team_id == group_team_stats_db.team_id
        assert team_stats.place == group_team_stats_db.place
        assert team_stats.team.name == group_team_stats_db.team.name
        assert team_stats.team.url == group_team_stats_db.team.url

    @pytest.mark.asyncio
    async def test_tournaments_get_group_calendar(self, get_async_db, create_env, group_db, game_db):
        games = await GroupDAO(get_async_db).get_group_calendar(group_db.name, group_db.tournament_id)

        assert len(games) == 1
        game = games[0]
        assert game.id == game_db.id
        assert game.home_team_id == game_db.home_team_id
        assert game.home_team_id == game_db.home_team_id
        assert game.home_team.name == game_db.home_team.name
        assert game.guest_team.name == game_db.guest_team.name
        assert game.result == game_db.result

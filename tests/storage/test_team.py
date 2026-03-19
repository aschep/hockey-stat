from hockey_stat.core.models import TeamInfo
from hockey_stat.storage.repository import TeamRepository


class TestTeamRepository:

    @staticmethod
    def check_team(result, expected):
        assert result.name == expected.name
        assert result.city == expected.city
        assert result.url == expected.url

    def test_save_team(self, get_db, team):
        saved = TeamRepository(get_db).save(team)
        self.check_team(saved, team)

    def test_found_team_by_name(self, get_db, team, team_db):
        found = TeamRepository(get_db).find_by_name(team.name)
        assert found
        self.check_team(found, team)

    def test_found_team_by_url(self, get_db, team, team_db):
        found = TeamRepository(get_db).find_by_url(team.url)
        assert found
        self.check_team(found, team)

    def test_update_team(self, get_db, team, team_db):
        team_new = TeamInfo(
            name="new " + team.name,
            city="new " + team.city,
            url=team.url,
        )

        found = TeamRepository(get_db).save(team_new)
        assert found
        assert found.url == team_db.url
        self.check_team(found, team_new)

from hockey_stat.core.models import TeamGroupStats
from hockey_stat.storage.repository import TeamGroupStatsRepository


class TestGroupTeamRepository:
    @staticmethod
    def check_stats(result, expected, expected_group_id, expected_team_id):
        assert result.group_id == expected_group_id
        assert result.team_id == expected_team_id
        assert result.games == expected.games
        assert result.wins == expected.wins
        assert result.wins_ot == expected.wins_ot
        assert result.wins_st == expected.wins_st
        assert result.loss == expected.loss
        assert result.loss_ot == expected.loss_ot
        assert result.loss_st == expected.loss_st
        assert result.goal_scored == expected.goal_scored
        assert result.goal_allowed == expected.goal_allowed
        assert result.plus_minus == expected.plus_minus
        assert result.points == expected.points

    def test_group_team_stats_save(self, get_db, group_team_stats, group_db, team_db):
        saved = TeamGroupStatsRepository(get_db).save(group_team_stats, group_db.id)

        self.check_stats(saved, group_team_stats, group_db.id, team_db.id)

    def test_group_team_stats_find(self, get_db, group_team_stats_db):
        found = TeamGroupStatsRepository(get_db).find_team_stats_in_group(
            group_team_stats_db.group_id, group_team_stats_db.team_id
        )

        self.check_stats(found, group_team_stats_db, group_team_stats_db.group_id, group_team_stats_db.team_id)

    def test_group_team_stats_save_raise_if_no_team(self, get_db):
        stats = TeamGroupStats(
            place=2,
            name="some",
            city="some",
            games=10,
            wins=6,
            wins_ot=2,
            wins_st=0,
            loss=0,
            loss_ot=1,
            loss_st=1,
            goal_scored=54,
            goal_allowed=34,
            plus_minus=20,
            points=18,
            url="some",
        )

        assert not TeamGroupStatsRepository(get_db).save(stats, 1)

    def test_group_team_stats_update(self, get_db, group_team_stats, group_team_stats_db):
        group_team_stats.place = 4
        group_team_stats.games = 15
        group_team_stats.wins = 8
        group_team_stats.wins_ot = 2
        group_team_stats.wins_st = 0
        group_team_stats.loss = 3
        group_team_stats.loss_ot = 1
        group_team_stats.loss_st = 1
        group_team_stats.goal_scored = 75
        group_team_stats.goal_allowed = 48
        group_team_stats.plus_minus = 27
        group_team_stats.points = 22

        updated = TeamGroupStatsRepository(get_db).save(group_team_stats, group_team_stats_db.group_id)
        self.check_stats(updated, group_team_stats, group_team_stats_db.group_id, group_team_stats_db.team_id)

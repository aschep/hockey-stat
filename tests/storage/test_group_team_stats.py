from datetime import datetime

from hockey_stat.core.models import Group, TeamGroupStats, TeamInfo, Tournament
from hockey_stat.storage.repository import (
    GroupRepository,
    TeamGroupStatsRepository,
    TeamRepository,
    TournamentRepository,
)


def prepare_env(db):
    repo = TournamentRepository(db)

    tournament = Tournament(
        name="blabla name",
        age=2123,
        url="tournament_url",
        key="tournament_key",
    )
    tour_db = repo.save(tournament)

    repo = GroupRepository(db)
    group = Group(name="super group", url="group url", key="group key")

    group_db = repo.save(group, tour_db.id)

    team_repo = TeamRepository(db)
    team = TeamInfo(
        name="team1",
        city="team city",
        url="/teams/team_1/",
    )
    team_db = team_repo.save(team)
    return group_db, team_db


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


def test_group_team_stats_save(get_db):
    group, team = prepare_env(get_db)

    repo = TeamGroupStatsRepository(get_db)

    stats = TeamGroupStats(
        place=2,
        name=team.name,
        city=team.city,
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
        url=team.url,
    )

    saved = repo.save(stats, group.id)

    check_stats(saved, stats, group.id, team.id)


def test_group_team_stats_find(get_db):
    group, team = prepare_env(get_db)

    repo = TeamGroupStatsRepository(get_db)

    stats = TeamGroupStats(
        place=2,
        name=team.name,
        city=team.city,
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
        url=team.url,
    )

    repo.save(stats, group.id)
    found = repo.find_team_stats_in_group(team.id, group.id)

    check_stats(found, stats, group.id, team.id)


def test_group_team_stats_save_raise_if_no_team(get_db):
    repo = TeamGroupStatsRepository(get_db)

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

    assert not repo.save(stats, 1)


def test_group_team_stats_update(get_db):
    group, team = prepare_env(get_db)

    repo = TeamGroupStatsRepository(get_db)

    stats1 = TeamGroupStats(
        place=2,
        name=team.name,
        city=team.city,
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
        url=team.url,
    )

    repo.save(stats1, group.id)

    stats2 = TeamGroupStats(
        place=4,
        name=team.name,
        city=team.city,
        games=15,
        wins=8,
        wins_ot=2,
        wins_st=0,
        loss=3,
        loss_ot=1,
        loss_st=1,
        goal_scored=75,
        goal_allowed=48,
        plus_minus=27,
        points=22,
        url=team.url,
    )

    updated = repo.save(stats2, group.id)
    check_stats(updated, stats2, group.id, team.id)

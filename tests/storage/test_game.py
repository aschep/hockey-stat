from datetime import datetime

from hockey_stat.core.models import Game, Group, TeamInfo, Tournament
from hockey_stat.storage.repository import GameRepository, GroupRepository, TeamRepository, TournamentRepository


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
    home_team = TeamInfo(
        name="team1",
        city="team city",
        url="/teams/team_1/",
    )
    guest_team = TeamInfo(
        name="team2",
        city="team city",
        url="/teams/team_2/",
    )
    home_team_db = team_repo.save(home_team)
    guest_team_db = team_repo.save(guest_team)

    return group_db, home_team_db, guest_team_db


def check_game(result, expected, group_id, home_id, guest_id):
    assert result.number == expected.number
    assert result.date == expected.date
    assert result.group_id == group_id
    assert result.home_team_id == home_id
    assert result.guest_team_id == guest_id
    assert result.result == expected.result
    assert result.url == expected.url


def test_game_save(get_db):
    group, home, guest = prepare_env(get_db)

    game = Game(
        number=13,
        date=datetime.now(None),
        home_team="home team",
        guest_team="guest team",
        result="2:3",
        url="game_url",
    )

    repo = GameRepository(get_db)
    saved = repo.save(game, group.id, home.id, guest.id)

    check_game(saved, game, group.id, home.id, guest.id)


def test_game_find_by_url(get_db):
    group, home, guest = prepare_env(get_db)

    game = Game(
        number=13,
        date=datetime.now(None),
        home_team="home team",
        guest_team="guest team",
        result="2:3",
        url="game_url",
    )

    repo = GameRepository(get_db)
    repo.save(game, group.id, home.id, guest.id)

    found = repo.find_by_url(game.url)
    check_game(found, game, group.id, home.id, guest.id)


def test_game_update(get_db):
    group, home, guest = prepare_env(get_db)

    game = Game(
        number=13,
        date=datetime.now(None),
        home_team="home team",
        guest_team="guest team",
        result="",
        url="game_url",
    )

    repo = GameRepository(get_db)
    repo.save(game, group.id, home.id, guest.id)

    game.result = "2:3"
    saved = repo.save(game, group.id, home.id, guest.id)

    check_game(saved, game, group.id, home.id, guest.id)

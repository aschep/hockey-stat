from hockey_stat.core.models import Player, TeamInfo
from hockey_stat.storage.repository import PlayerRepository, TeamRepository


def test_save_team(get_db):
    repo = TeamRepository(get_db)

    team = TeamInfo(
        "team name",
        "/teams/sdfsdfsdfsdfsdfsdfsdfsdf_2342348/",
    )
    saved = repo.save(team)
    assert saved.name == team.name
    assert saved.url == team.url


def test_found_team_by_name(get_db):
    repo = TeamRepository(get_db)

    team = TeamInfo(
        "team name",
        "/teams/sdfsdfsdfsdfsdfsdfsdfsdf_2342348/",
    )
    saved = repo.save(team)
    assert saved.name == team.name

    found = repo.find_by_name(team.name)
    assert found
    assert found.name == team.name
    assert found.url == team.url


def test_update_team(get_db):
    repo = TeamRepository(get_db)

    team = TeamInfo(
        "team name",
        "/teams/sdfsdfsdfsdfsdfsdfsdfsdf_2342348/",
    )
    saved = repo.save(team)
    assert saved.name == team.name

    team_new = TeamInfo(
        "team name",
        "/teams/new_url/",
    )
    found = repo.save(team_new)
    assert found
    assert found.name == team.name
    assert found.url == team_new.url


def check_player(player: Player, saved: Player):
    assert saved.name == player.name
    assert saved.player_id == player.player_id
    assert saved.player_url == player.player_url
    assert saved.number == player.number
    assert saved.grip == player.grip
    assert saved.height == player.height
    assert saved.weight == player.weight


def test_save_player(get_db):
    player_repo = PlayerRepository(get_db)
    team_repo = TeamRepository(get_db)

    team = TeamInfo(
        "team name",
        "/teams/sdfsdfsdfsdfsdfsdfsdfsdf_2342348/",
    )
    saved_team = team_repo.save(team)

    player = Player(
        "2342348",
        "/player/sdfsdfsdfsdfsdfsdfsdfsdf-2013-44-11-2342348/",
        "Игрок 1",
        "01-01_2001",
        "Защ",
        "Левый",
        "45",
        "130",
        "SuperPuper",
        4,
    )
    saved = player_repo.save(player, saved_team.id)
    check_player(player, saved)
    assert saved.team_id == saved_team.id


def test_find_player_by_player_id(get_db):
    player_repo = PlayerRepository(get_db)
    team_repo = TeamRepository(get_db)

    team = TeamInfo(
        "team name",
        "/teams/sdfsdfsdfsdfsdfsdfsdfsdf_2342348/",
    )
    saved_team = team_repo.save(team)

    player = Player(
        "2342348",
        "/player/sdfsdfsdfsdfsdfsdfsdfsdf-2013-44-11-2342348/",
        "Игрок 1",
        "01-01_2001",
        "Защ",
        "Левый",
        "45",
        "130",
        "SuperPuper",
        4,
    )
    saved = player_repo.save(player, saved_team.id)
    assert saved.name == player.name

    found = player_repo.find_by_id(player.player_id)

    check_player(player, found)
    assert found.team_id == saved_team.id

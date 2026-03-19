from hockey_stat.core.models import Group, Tournament
from hockey_stat.storage.models import GroupDB
from hockey_stat.storage.repository import GroupRepository, TournamentRepository


def save_tournament(db):
    repo = TournamentRepository(db)

    tournament = Tournament(
        name="blabla name",
        age=2123,
        url="tournament_url",
        key="tournament_key",
    )
    return repo.save(tournament)


def check_group(result, expected, tid):
    assert result.tournament_id == tid
    assert result.name == expected.name
    assert result.url == expected.url
    assert result.key == expected.key


def test_group_save(get_db):
    tournament = save_tournament(get_db)

    repo = GroupRepository(get_db)
    group = Group(name="super group", url="group url", key="group key")

    saved = repo.save(group, tournament.id)
    check_group(saved, group, tournament.id)


def test_group_find(get_db):
    tournament = save_tournament(get_db)

    repo = GroupRepository(get_db)
    group = Group(name="super group", url="group url", key="group key")

    saved = repo.save(group, tournament.id)
    check_group(saved, group, tournament.id)

    found = repo.find_by_name_tournament_id(tournament.id, group.name)
    check_group(found, group, tournament.id)


def test_group_update(get_db):
    tournament = save_tournament(get_db)

    repo = GroupRepository(get_db)
    group = Group(name="super group", url="group url", key="group key")

    saved = repo.save(group, tournament.id)
    check_group(saved, group, tournament.id)

    group1 = Group(name="super group", url="poper url", key="poper key")
    saved1 = repo.save(group1, tournament.id)

    check_group(saved1, group1, tournament.id)
    assert saved1.name == group.name
    assert saved1.url != group.url
    assert saved1.key != group.key
    assert saved1.tournament_id == tournament.id

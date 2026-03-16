from hockey_stat.core.models import Tournament
from hockey_stat.storage.repository import TournamentRepository


def check_tournament(result, expected):
    assert result.name == expected.name
    assert result.age == expected.age
    assert result.url == expected.url
    assert result.key == expected.key


def test_save_tournament_save(get_db):
    repo = TournamentRepository(get_db)

    tournament = Tournament(
        name="blabla name",
        age=2123,
        url="tournament_url",
        key="tournament_key",
    )
    saved = repo.save(tournament)
    check_tournament(saved, tournament)


def test_tournament_find(get_db):
    repo = TournamentRepository(get_db)

    tournament = Tournament(
        name="blabla name",
        age=2123,
        url="tournament_url",
        key="tournament_key",
    )
    saved = repo.save(tournament)
    found = repo.find_by_name_age(tournament.name, tournament.age)

    check_tournament(found, saved)


def test_tournament_update(get_db):
    repo = TournamentRepository(get_db)

    tournament = Tournament(
        name="blabla name",
        age=2123,
        url="tournament_url",
        key="tournament_key",
    )
    saved = repo.save(tournament)
    check_tournament(saved, tournament)

    tournament1 = Tournament(
        name="blabla name",
        age=2123,
        url="tournament_url_123",
        key="tournament_key_123",
    )
    saved = repo.save(tournament1)
    check_tournament(saved, tournament1)

    tournament2 = Tournament(
        name="blabla name",
        age=2223,
        url="tournament_url_123111",
        key="tournament_key_123111",
    )
    saved = repo.save(tournament2)
    check_tournament(saved, tournament2)

    found = repo.find_by_name_age(tournament.name, tournament.age)
    check_tournament(found, tournament1)

    assert found.name == saved.name
    assert found.age != saved.age
    assert found.url != saved.url
    assert found.key != saved.key

from hockey_stat.core.models import Tournament
from hockey_stat.storage.repository import TournamentRepository


class TestTournamentRepository:
    @staticmethod
    def check_tournament(result, expected):
        assert result.name == expected.name
        assert result.age == expected.age
        assert result.url == expected.url
        assert result.key == expected.key

    def test_save_tournament_save(self, get_db, tournament):
        repo = TournamentRepository(get_db)

        saved = repo.save(tournament)
        self.check_tournament(saved, tournament)

    def test_tournament_find(self, get_db, tournament_db):
        found = TournamentRepository(get_db).find_by_name_age(tournament_db.name, tournament_db.age)

        self.check_tournament(found, tournament_db)

    def test_tournament_update(self, get_db, tournament_db):
        tournament1 = Tournament(
            name="blabla name",
            age=2123,
            url="tournament_url_123",
            key="tournament_key_123",
        )
        saved = TournamentRepository(get_db).save(tournament1)
        self.check_tournament(saved, tournament1)

        tournament2 = Tournament(
            name="blabla name",
            age=2223,
            url="tournament_url_123111",
            key="tournament_key_123111",
        )
        saved = TournamentRepository(get_db).save(tournament2)
        self.check_tournament(saved, tournament2)

        found = TournamentRepository(get_db).find_by_name_age(tournament_db.name, tournament_db.age)
        self.check_tournament(found, tournament1)

        assert found.name == saved.name
        assert found.age != saved.age
        assert found.url != saved.url
        assert found.key != saved.key

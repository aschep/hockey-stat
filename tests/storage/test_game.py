from hockey_stat.storage.repository import GameRepository


class TestGameRepository:
    @staticmethod
    def check_game(result, expected, group_id, home_id, guest_id):
        assert result.number == expected.number
        assert result.date == expected.date
        assert result.group_id == group_id
        assert result.home_team_id == home_id
        assert result.guest_team_id == guest_id
        assert result.result == expected.result
        assert result.url == expected.url

    def test_game_save(self, get_db, game, group_db, home_guest_db):
        home_db, guest_db = home_guest_db
        saved = GameRepository(get_db).save(game, group_db.id, home_db.id, guest_db.id)

        self.check_game(saved, game, group_db.id, home_db.id, guest_db.id)

    def test_game_find_by_url(self, get_db, game_db):
        found = GameRepository(get_db).find_by_url(game_db.url)
        self.check_game(found, game_db, game_db.group_id, game_db.home_team_id, game_db.guest_team_id)

    def test_game_update(self, get_db, game, game_db):
        game.result = "2:3"
        saved = GameRepository(get_db).save(game, game_db.group_id, game_db.home_team_id, game_db.guest_team_id)
        self.check_game(saved, game, game_db.group_id, game_db.home_team_id, game_db.guest_team_id)

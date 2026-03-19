from hockey_stat.core.models import Player
from hockey_stat.storage.repository import PlayerRepository


class TestPlayerRepository:

    @staticmethod
    def check_player(player: Player, saved: Player):
        assert saved.name == player.name
        assert saved.player_id == player.player_id
        assert saved.player_url == player.player_url
        assert saved.number == player.number
        assert saved.grip == player.grip
        assert saved.height == player.height
        assert saved.weight == player.weight

    def test_save_player(self, get_db, team_db, player):
        saved = PlayerRepository(get_db).save(player, team_db.id)
        self.check_player(player, saved)
        assert saved.team_id == team_db.id

    def test_find_player_by_player_id(self, get_db, player, player_db):
        found = PlayerRepository(get_db).find_by_id(player.player_id)

        self.check_player(player, found)
        assert found.team_id == player_db.team_id

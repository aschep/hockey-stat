from hockey_stat.player import PlayerParser


def read_file(filename: str) -> str:
    print("mocker call")
    with open(filename, "r") as fp:
        content = fp.read()
        return content


def test_parser_player_info(monkeypatch):
    monkeypatch.setattr("hockey_stat.player.make_request", read_file)

    player = PlayerParser("11111111", "tests/data/player_stat.html").parse()

    assert player
    assert player.name == "Игрок Защитникович Нападающий"
    assert player.birthday == "16.11.2013 (11 лет)"
    assert player.school == 'ХК "Супер Команда"\n(Какая-то область)'
    assert player.position == "Защитник"
    assert player.weight == "50"
    assert player.height == "162"
    assert player.grip == "Правый"


def test_parser_player_game_stats(monkeypatch):
    monkeypatch.setattr("hockey_stat.player.make_request", read_file)

    parser = PlayerParser("11111111", "tests/data/player_stat.html")
    parser.player_stats_url = "tests/data/player_games_stat.json"

    games_stat = parser.parse_stats()

    assert len(games_stat) == 6

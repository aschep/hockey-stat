from hockey_stat.parsers.player import PlayerParser
from tests.conftest import read_file


def test_parser_player_info(monkeypatch):
    monkeypatch.setattr("hockey_stat.parsers.player.make_request", read_file)

    player = PlayerParser("11111111", 1, "tests/data/player_stat.html").parse()

    assert player
    assert player.name == "Игрок Защитникович Нападающий"
    assert player.number == 1
    assert player.player_id == "11111111"
    assert player.player_url == "tests/data/player_stat.html"
    assert player.birthday == "16.11.2013 (11 лет)"
    assert player.school == 'ХК "Супер Команда"'
    assert player.position == "Нападающий"
    assert player.weight == "50"
    assert player.height == "162"
    assert player.grip == "Левый"


def test_parser_player_game_stats(monkeypatch):
    monkeypatch.setattr("hockey_stat.parsers.player.make_request", read_file)

    parser = PlayerParser("11111111", 1, "tests/data/player_stat.html")
    parser.player_stats_url = "tests/data/player_games_stat.json"

    games_stat = parser.parse_stats()

    assert len(games_stat) == 3

    game1 = games_stat[0]
    assert game1.tournament == "Первенство XX лет"
    assert game1.date == "29.09.2042"
    assert game1.teams == "КОМАНДА 1 : КОМАНДА 2"
    assert game1.score == "5:2"
    assert game1.goals == 0
    assert game1.assists == 0
    assert game1.points == 0
    assert game1.plus == 2
    assert game1.minus == 0
    assert game1.plus_minus == 1

    game1 = games_stat[1]
    assert game1.tournament == "Первенство XX лет"
    assert game1.date == "28.09.2042"
    assert game1.teams == "КОМАНДА 1 : КОМАНДА 2"
    assert game1.score == "4:3 ПБ"
    assert game1.goals == 0
    assert game1.assists == 0
    assert game1.points == 0
    assert game1.plus == 2
    assert game1.minus == 1
    assert game1.plus_minus == 0

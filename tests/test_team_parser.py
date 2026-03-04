from hockey_stat.player import Player
from tests.conftest import read_file
from hockey_stat.team import TeamParser


class PlayerParserMock:
    items = [
        Player("111111111", "some url", "Игрок 1", "01-01_2001", "Защ", "Левый", "45", "130", "SuperPuper", 1),
        Player("222222222", "some url","Игрок 2", "01-10_2001", "Нап", "Правый", "55", "160", "SuperPuper", 2),
        Player("333333333", "some url","Игрок 3", "11-04_2001", "Врат", "Левый", "47", "150", "SuperPuper", 3),
    ]
    counter = 0

    def __init__(self, _: str, __: str): ...

    def parse(self):
        idx = self.counter
        PlayerParserMock.counter += 1
        return self.items[idx]


def test_parser_player_info(monkeypatch):
    monkeypatch.setattr("hockey_stat.team.make_request", read_file)
    monkeypatch.setattr("hockey_stat.team.PlayerParser", PlayerParserMock)

    parser = TeamParser("Some Team", "tests/data/team_info.html")
    parser.parse()

    assert parser._team.name == "Some Team"
    assert parser._team.url == "tests/data/team_info.html"
    players = parser._team.players
    assert len(players) == 3
    for idx, player in enumerate(players):
        assert player == PlayerParserMock.items[idx]

from hockey_stat.core.models import Player
from hockey_stat.parsers.team import TeamParser
from tests.conftest import read_file


class PlayerParserMock:
    items = [
        Player(
            "",
            "some url",
            "Игрок 1",
            "01-01_2001",
            "Защ",
            "Левый",
            "45",
            "130",
            "SuperPuper",
            1,
        ),
        Player(
            "",
            "some url",
            "Игрок 2",
            "01-10_2001",
            "Нап",
            "Правый",
            "55",
            "160",
            "SuperPuper",
            2,
        ),
        Player(
            "",
            "some url",
            "Игрок 3",
            "11-04_2001",
            "Врат",
            "Левый",
            "47",
            "150",
            "SuperPuper",
            3,
        ),
    ]
    counter = 0

    def __init__(self, _id: str, n: int, _u: str):
        self._number = n
        self._id = _id
        self._url = _u

    def parse(self):
        idx = self.counter
        PlayerParserMock.counter += 1
        self.items[idx].number = self._number
        self.items[idx].player_id = self._id
        self.items[idx].player_url = self._url
        return self.items[idx]


def test_parser_player_info(monkeypatch):
    monkeypatch.setattr("hockey_stat.parsers.team.make_request", read_file)
    monkeypatch.setattr("hockey_stat.parsers.team.PlayerParser", PlayerParserMock)

    parser = TeamParser("Some Team", "tests/data/team_info.html")
    parser.parse()

    assert parser._team.name == "Some Team"
    assert parser._team.url == "tests/data/team_info.html"
    players = parser._team.players
    assert len(players) == 3

    expected = [
        Player(
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
        ),
        Player(
            "3453453",
            "/player/sdfsdfsdfsdfsf-2013-45-92-3453453/",
            "Игрок 2",
            "01-10_2001",
            "Нап",
            "Правый",
            "55",
            "160",
            "SuperPuper",
            5,
        ),
        Player(
            "345345345",
            "/player/sdrsdfsdfsdfsdf-2013-88-28-345345345/",
            "Игрок 3",
            "11-04_2001",
            "Врат",
            "Левый",
            "47",
            "150",
            "SuperPuper",
            27,
        ),
    ]
    for exp, player in zip(expected, players):
        assert player == exp

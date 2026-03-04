import typing as t
from dataclasses import asdict
from dataclasses import dataclass, field


@dataclass
class PlayerGameStat:
    tournament: str
    date: str
    score: str
    teams: str
    goals: int
    assists: int
    points: int
    plus: int
    minus: int
    plus_minus: int


@dataclass
class Player:
    player_id: str
    player_url: str
    name: str
    birthday: str
    position: str
    grip: str
    weight: str
    height: str
    school: str
    number: int

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class TeamInfo:
    name: str
    url: str
    players: t.List[Player] = field(default_factory=list)

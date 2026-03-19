import typing as t
from dataclasses import asdict, dataclass, field
from datetime import datetime


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
    city: str
    url: str
    players: t.List[Player] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Game:
    number: int
    date: datetime
    home_team: str
    guest_team: str
    result: str
    url: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class TeamGroupStats:
    place: int
    name: str
    city: str
    games: int
    wins: int
    wins_ot: int
    wins_st: int
    loss: int
    loss_ot: int
    loss_st: int
    goal_scored: int
    goal_allowed: int
    plus_minus: int
    points: int
    url: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Group:
    name: str
    url: str
    key: str
    teams: t.List[TeamGroupStats] = field(default_factory=list)
    games: t.List[Game] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Tournament:
    name: str
    age: int
    url: str
    key: str
    groups: t.List[Group] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

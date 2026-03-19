from datetime import datetime

import pytest

from hockey_stat.core.models import (
    Game,
    Group,
    Player,
    TeamGroupStats,
    TeamInfo,
    Tournament,
)
from hockey_stat.storage.database import SessionLocal
from hockey_stat.storage.repository import (
    GameRepository,
    GroupRepository,
    PlayerRepository,
    TeamGroupStatsRepository,
    TeamRepository,
    TournamentRepository,
)


@pytest.fixture
def client():
    """HTTP клиент мок"""
    return "mocked html"


def read_file(filename: str, params=None) -> str:
    with open(filename, "r") as fp:
        return fp.read()


@pytest.fixture(scope="function")
def get_db():
    """Sync DB сессия для тестов"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()


@pytest.fixture
def tournament():
    yield Tournament(
        name="blabla name",
        age=2123,
        url="tournament_url",
        key="tournament_key",
    )


@pytest.fixture(scope="function")
def tournament_db(get_db, tournament):
    yield TournamentRepository(get_db).save(tournament)


@pytest.fixture
def group():
    yield Group(name="super group", url="group url", key="group key")


@pytest.fixture(scope="function")
def group_db(get_db, tournament_db, group):
    yield GroupRepository(get_db).save(group, tournament_db.id)


@pytest.fixture
def team():
    yield TeamInfo(
        name="team name",
        city="team city",
        url="/teams/team_url_2342348/",
    )


@pytest.fixture(scope="function")
def team_db(get_db, team):
    yield TeamRepository(get_db).save(team)


@pytest.fixture(scope="function")
def home_guest_db(get_db):
    home = TeamInfo(
        name="home team name",
        city="home team city",
        url="/teams/home_team_url_2342348/",
    )
    guest = TeamInfo(
        name="guest team name",
        city="guest team city",
        url="/teams/guest_team_url_2342348/",
    )
    repo = TeamRepository(get_db)
    yield repo.save(home), repo.save(guest)


@pytest.fixture
def player():
    yield Player(
        "2342348",
        "/player/player-2013-44-11-2342348/",
        "Игрок 1",
        "01-01_2001",
        "Защ",
        "Левый",
        "45",
        "130",
        "SuperPuper",
        4,
    )


@pytest.fixture
def player_db(get_db, player, team_db):
    yield PlayerRepository(get_db).save(player, team_db.id)


@pytest.fixture
def game():
    yield Game(
        number=13,
        date=datetime.now(None),
        home_team="home team",
        guest_team="guest team",
        result="2:3",
        url="game_url",
    )


@pytest.fixture
def game_db(get_db, game, group_db, home_guest_db):
    home_db, guest_db = home_guest_db
    yield GameRepository(get_db).save(game, group_db.id, home_db.id, guest_db.id)


@pytest.fixture
def group_team_stats(team_db):
    yield TeamGroupStats(
        place=2,
        name=team_db.name,
        city=team_db.city,
        games=10,
        wins=6,
        wins_ot=2,
        wins_st=0,
        loss=0,
        loss_ot=1,
        loss_st=1,
        goal_scored=54,
        goal_allowed=34,
        plus_minus=20,
        points=18,
        url=team_db.url,
    )


@pytest.fixture
def group_team_stats_db(get_db, group_team_stats, group_db):
    yield TeamGroupStatsRepository(get_db).save(group_team_stats, group_db.id)

from sqlalchemy.orm import Session

from hockey_stat.core.models import Player, TeamInfo, Tournament

from ..core.models import Group
from .models import GroupDB, PlayerDB, TeamDB, TournamentDB


class TournamentRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, tour: Tournament) -> TournamentDB:
        db_tour = self.find_by_name_age(tour.name, tour.age)
        if not db_tour:
            db_tour = TournamentDB(name=tour.name, age=tour.age, url=tour.url, key=tour.key)
        else:
            db_tour.url = tour.url
            db_tour.key = tour.key

        self.db.merge(db_tour)
        self.db.flush()
        return db_tour

    def find_by_name_age(self, name: str, age: int) -> TournamentDB:
        return self.db.query(TournamentDB).filter(TournamentDB.name == name, TournamentDB.age == age).first()


class GroupRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, group: Group, tournament_id: int) -> GroupDB:
        db_group = self.find_by_name_tournament_id(tournament_id, group.name)
        if not db_group:
            db_group = GroupDB(name=group.name, url=group.url, key=group.key, tournament_id=tournament_id)
        else:
            db_group.url = group.url
            db_group.key = group.key

        self.db.merge(db_group)
        self.db.flush()
        return db_group

    def find_by_name_tournament_id(self, tournament_id: int, name: str) -> TournamentDB:
        return self.db.query(GroupDB).filter(GroupDB.name == name, GroupDB.tournament_id == tournament_id).first()


class TeamRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, team: TeamInfo) -> TeamDB:
        db_team = self.find_by_url(team.url)
        if not db_team:
            db_team = TeamDB(**(team.to_dict()))
        else:
            db_team.city = team.city
            db_team.name = team.name

        db_team = self.db.merge(db_team)
        self.db.flush()
        return db_team

    def find_by_name(self, name: str) -> TeamDB:
        return self.db.query(TeamDB).filter(TeamDB.name == name).first()

    def find_by_url(self, url: str) -> TeamDB:
        return self.db.query(TeamDB).filter(TeamDB.url == url).first()


class PlayerRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, player: Player, team_id: int):
        db_player = self.db.merge(PlayerDB(team_id=team_id, **player.to_dict()))
        self.db.flush()
        return db_player

    def find_by_id(self, player_id: str) -> PlayerDB:
        return self.db.query(PlayerDB).filter(PlayerDB.player_id == player_id).first()

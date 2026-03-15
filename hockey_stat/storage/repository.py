from sqlalchemy.orm import Session

from hockey_stat.core.models import Player, TeamInfo

from .models import PlayerDB, TeamDB


class TeamRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, team: TeamInfo) -> TeamDB:
        db_team = self.find_by_name(team.name)
        if not db_team:
            db_team = TeamDB(name=team.name, url=team.url)
        else:
            db_team.url = team.url
        self.db.merge(db_team)
        self.db.flush()
        return db_team

    def find_by_name(self, name: str) -> TeamDB:
        return self.db.query(TeamDB).filter(TeamDB.name == name).first()


class PlayerRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, player: Player, team_id: int):
        db_player = self.db.merge(PlayerDB(team_id=team_id, **player.to_dict()))
        self.db.flush()
        return db_player

    def find_by_id(self, player_id: str) -> PlayerDB:
        return self.db.query(PlayerDB).filter(PlayerDB.player_id == player_id).first()

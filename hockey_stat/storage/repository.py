import typing as t

from sqlalchemy.orm import Session

from hockey_stat.core.models import Game, Group, Player, TeamGroupStats, TeamInfo, Tournament

from .models import GameDB, GroupDB, PlayerDB, TeamDB, TeamGroupStatsDB, TournamentDB


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

        db_tour = self.db.merge(db_tour)
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

        db_group = self.db.merge(db_group)
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


class GameRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, game: Game, group_id: int, home_id: int, guest_id: int) -> GameDB:
        db_game = self.find_by_url(game.url)
        if not db_game:
            db_game = GameDB(
                number=game.number,
                date=game.date,
                group_id=group_id,
                home_team_id=home_id,
                guest_team_id=guest_id,
                result=game.result,
                url=game.url,
            )
        else:
            db_game.number = game.number
            db_game.date = game.date
            db_game.group_id = group_id
            db_game.home_team_id = home_id
            db_game.guest_team_id = guest_id
            db_game.result = game.result

        db_game = self.db.merge(db_game)
        self.db.flush()
        return db_game

    def find_by_url(self, url: str) -> GameDB:
        return self.db.query(GameDB).filter(GameDB.url == url).first()


class TeamGroupStatsRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, stat: TeamGroupStats, group_id: int) -> t.Optional[TeamGroupStatsDB]:
        team_repo = TeamRepository(self.db)
        db_team = team_repo.find_by_url(stat.url)
        if not db_team:
            return None

        db_stats = self.find_team_stats_in_group(db_team.id, group_id)
        if not db_stats:
            db_stats = TeamGroupStatsDB(
                group_id=group_id,
                team_id=db_team.id,
                place=stat.place,
                games=stat.games,
                wins=stat.wins,
                wins_ot=stat.wins_ot,
                wins_st=stat.wins_st,
                loss=stat.loss,
                loss_ot=stat.loss_ot,
                loss_st=stat.loss_st,
                goal_scored=stat.goal_scored,
                goal_allowed=stat.goal_allowed,
                plus_minus=stat.plus_minus,
                points=stat.points,
            )
        else:
            db_stats.place = stat.place
            db_stats.games = stat.games
            db_stats.wins = stat.wins
            db_stats.wins_ot = stat.wins_ot
            db_stats.wins_st = stat.wins_st
            db_stats.loss = stat.loss
            db_stats.loss_ot = stat.loss_ot
            db_stats.loss_st = stat.loss_st
            db_stats.goal_scored = stat.goal_scored
            db_stats.goal_allowed = stat.goal_allowed
            db_stats.plus_minus = stat.plus_minus
            db_stats.points = stat.points
        db_stats = self.db.merge(db_stats)
        self.db.flush()
        return db_stats

    def find_team_stats_in_group(self, team_id: int, group_id: int) -> TeamGroupStatsDB:
        return (
            self.db.query(TeamGroupStatsDB)
            .filter(TeamGroupStatsDB.team_id == team_id, TeamGroupStatsDB.group_id == group_id)
            .first()
        )


class PlayerRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, player: Player, team_id: int):
        db_player = self.db.merge(PlayerDB(team_id=team_id, **player.to_dict()))
        self.db.flush()
        return db_player

    def find_by_id(self, player_id: str) -> PlayerDB:
        return self.db.query(PlayerDB).filter(PlayerDB.player_id == player_id).first()

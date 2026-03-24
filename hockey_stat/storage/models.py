from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, UniqueConstraint
from sqlalchemy.orm import declarative_base, mapped_column, relationship

Base = declarative_base()


class TournamentDB(Base):
    __tablename__ = "tournaments"

    id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer, nullable=False)
    name = Column(Text, nullable=False)
    url = Column(Text, nullable=False)
    key = Column(Text, nullable=False)

    __table_args__ = (UniqueConstraint("name", "age", name="name_age_uc"),)

    groups = relationship("GroupDB", back_populates="tournament", cascade="save-update, merge, delete")


class GroupDB(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    tournament_id = Column(Integer, ForeignKey("tournaments.id"), nullable=False)
    name = Column(Text, nullable=False)
    url = Column(Text, nullable=False)
    key = Column(Text, nullable=False)

    __table_args__ = (UniqueConstraint("name", "tournament_id", name="name_tournament_id_uc"),)

    tournament = relationship("TournamentDB", back_populates="groups")
    games = relationship("GameDB", back_populates="group", cascade="save-update, merge, delete")
    teams = relationship("TeamGroupStatsDB", back_populates="group", cascade="save-update, merge, delete")


class GameDB(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    group_id = mapped_column(Integer, ForeignKey("groups.id"))
    number = Column(Integer, nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    home_team_id = mapped_column(Integer, ForeignKey("teams.id"))
    guest_team_id = mapped_column(Integer, ForeignKey("teams.id"))
    result = Column(Text, nullable=False)
    url = Column(Text, nullable=False)

    group = relationship("GroupDB", back_populates="games")
    home_team = relationship("TeamDB", primaryjoin="GameDB.home_team_id == TeamDB.id")
    guest_team = relationship("TeamDB", primaryjoin="GameDB.guest_team_id == TeamDB.id")


class TeamGroupStatsDB(Base):
    __tablename__ = "team_group_stats"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    place = Column(Integer, nullable=False)
    games = Column(Integer, nullable=False)
    wins = Column(Integer, nullable=False)
    wins_ot = Column(Integer, nullable=False)
    wins_st = Column(Integer, nullable=False)
    loss = Column(Integer, nullable=False)
    loss_ot = Column(Integer, nullable=False)
    loss_st = Column(Integer, nullable=False)
    goal_scored = Column(Integer, nullable=False)
    goal_allowed = Column(Integer, nullable=False)
    plus_minus = Column(Integer, nullable=False)
    points = Column(Integer, nullable=False)

    group = relationship("GroupDB", back_populates="teams")
    team = relationship("TeamDB", primaryjoin="TeamGroupStatsDB.team_id == TeamDB.id")


class PlayerDB(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, nullable=False)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)

    player_id = Column(Text, unique=True, index=True, nullable=False)
    player_url = Column(Text, nullable=False)
    name = Column(Text, index=True, nullable=False)
    birthday = Column(Text, nullable=False)
    position = Column(Text, nullable=False)
    grip = Column(Text, nullable=False)
    weight = Column(Text, nullable=False)
    height = Column(Text, nullable=False)
    school = Column(Text, nullable=False)

    team = relationship("TeamDB", back_populates="players")
    # stats = relationship("PlayerStats", back_populates="player")


class TeamDB(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False, index=True)
    city = Column(Text)
    url = Column(Text, nullable=False, index=True, unique=True)

    players = relationship("PlayerDB", back_populates="team")


# class PlayerStatsDB(Base):
#     __tablename__ = "player_stats"
#
#     id = Column(Integer, primary_key=True)
#     player_id = Column(Integer, ForeignKey("players.id"))
#     game_id = Column(Text)
#     games = Column(Integer, default=0)
#     goals = Column(Integer, default=0)
#     assists = Column(Integer, default=0)
#     plus_minus = Column(Integer, default=0)
#
#     player = relationship("PlayerDB", back_populates="stats")

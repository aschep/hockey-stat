from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class TournamentDB(Base):
    __tablename__ = "tournaments"

    id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer, nullable=False)
    name = Column(Text, nullable=False)
    url = Column(Text, nullable=False)
    key = Column(Text, nullable=False)

    __table_args__ = (UniqueConstraint("name", "age", name="name_age_uc"),)

    groups = relationship("GroupDB", back_populates="tournament")


class GroupDB(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    tournament_id = Column(Integer, ForeignKey("tournaments.id"))
    name = Column(Text, nullable=False)
    url = Column(Text, nullable=False)
    key = Column(Text, nullable=False)

    __table_args__ = (UniqueConstraint("name", "tournament_id", name="name_tournament_id_uc"),)

    tournament = relationship("TournamentDB", back_populates="groups")
    games = relationship("GameDB", back_populates="group")


class GameDB(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"))
    number = Column(Integer, nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    home_team_id = Column(Integer, ForeignKey("teams.id"))
    guest_team_id = Column(Integer, ForeignKey("teams.id"))
    result = Column(Text, nullable=False)
    url = Column(Text, nullable=False)

    group = relationship("GroupDB", back_populates="games")
    home_team = relationship("TeamDB", primaryjoin="GameDB.home_team_id == TeamDB.id", lazy="joined")
    guest_team = relationship("TeamDB", primaryjoin="GameDB.guest_team_id == TeamDB.id", lazy="joined")


class PlayerDB(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer)
    team_id = Column(Integer, ForeignKey("teams.id"))

    player_id = Column(Text, unique=True, index=True)
    player_url = Column(Text)
    name = Column(Text, index=True)
    birthday = Column(Text)
    position = Column(Text)
    grip = Column(Text)
    weight = Column(Text)
    height = Column(Text)
    school = Column(Text)

    team = relationship("TeamDB", back_populates="players")
    # Связь с матчами (1:N)
    # stats = relationship("PlayerStats", back_populates="player")


class TeamDB(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, index=True)
    url = Column(Text)

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

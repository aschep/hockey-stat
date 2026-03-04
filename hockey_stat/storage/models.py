from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


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

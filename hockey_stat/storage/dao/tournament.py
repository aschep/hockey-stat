import typing as t
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import desc
from sqlalchemy.ext.asyncio import AsyncSession

from hockey_stat.storage.models import (
    GameDB,
    GroupDB,
    TeamDB,
    TeamGroupStatsDB,
    TournamentDB,
)


class TournamentDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> t.Sequence[TournamentDB]:
        result = await self.session.execute(sa.select(TournamentDB))
        return result.scalars().all()

    async def get_id(self, name: str, age: int) -> t.Optional[TournamentDB.id]:
        result = await self.session.execute(
            sa.select(TournamentDB.id).where(TournamentDB.name == name, TournamentDB.age == age)
        )
        return result.scalar()

    async def get_with_groups(self, name: str, age: int) -> t.Optional[TournamentDB]:
        result = await self.session.execute(
            sa.select(TournamentDB)
            .where(TournamentDB.name == name, TournamentDB.age == age)
            .options(sa.orm.joinedload(TournamentDB.groups))
        )
        return result.scalar()

    async def get_names(self) -> t.Sequence[str]:
        result = await self.session.execute(sa.select(TournamentDB.name).distinct())
        return result.scalars().all()

    async def get_ages(self, name: str) -> t.Sequence[int]:
        result = await self.session.execute(sa.select(TournamentDB.age).where(TournamentDB.name == name).distinct())
        return result.scalars().all()


class GroupDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_group_names(self, tour_id: int) -> t.Sequence[GroupDB.name]:
        result = await self.session.execute(sa.select(GroupDB.name).where(GroupDB.tournament_id == tour_id))
        return result.scalars().all()

    @staticmethod
    def get_subquery(name: str, tour_id: int) -> sa.Select[sa.Any]:
        return sa.select(GroupDB.id).where(GroupDB.tournament_id == tour_id, GroupDB.name == name)

    async def get_group_table(self, name: str, tour_id: int) -> t.Sequence[TeamGroupStatsDB]:
        result = await self.session.execute(
            sa.select(TeamGroupStatsDB)
            .options(sa.orm.joinedload(TeamGroupStatsDB.team))
            .where(TeamGroupStatsDB.group_id.in_(self.get_subquery(name, tour_id)))
        )
        return result.scalars().all()

    async def get_group_calendar(self, name: str, tour_id: int, from_now: bool = True) -> t.Sequence[GameDB]:
        condition = [GameDB.group_id.in_(self.get_subquery(name, tour_id))]
        if from_now:
            condition.append(GameDB.date >= datetime.today())

        query = (
            sa.select(GameDB)
            .options(
                sa.orm.joinedload(GameDB.home_team),
                sa.orm.joinedload(GameDB.guest_team),
            )
            .where(*condition)
            .order_by(GameDB.number)
            .limit(10)
        )

        result = await self.session.execute(query)
        return result.scalars().all()

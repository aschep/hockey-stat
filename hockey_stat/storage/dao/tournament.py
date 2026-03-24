import typing as t

import sqlalchemy as sa
from sqlalchemy import desc
from sqlalchemy.ext.asyncio import AsyncSession

from hockey_stat.storage.models import GameDB, GroupDB, TeamGroupStatsDB, TournamentDB


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
            sa.select(TournamentDB, GroupDB)
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

    async def get_group_table(self, name: str, tour_id: int) -> GroupDB:
        result = await self.session.execute(
            sa.select(GroupDB, TeamGroupStatsDB)
            .where(GroupDB.tournament_id == tour_id, GroupDB.name == name)
            .options(sa.orm.joinedload(GroupDB.teams), sa.orm.joinedload(TeamGroupStatsDB.team))
        )
        return result.scalar()

    async def get_group_calendar(self, name: str, tour_id: int) -> GroupDB:
        result = await self.session.execute(
            sa.select(GroupDB, GameDB)
            .where(GroupDB.tournament_id == tour_id, GroupDB.name == name)
            .options(
                sa.orm.joinedload(GroupDB.games),
                sa.orm.joinedload(GameDB.home_team),
                sa.orm.joinedload(GameDB.guest_team),
            )
            .order_by(desc(GameDB.date))
            .limit(10)
        )
        return result.scalar()

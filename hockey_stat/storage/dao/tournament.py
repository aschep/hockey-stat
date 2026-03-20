import typing as t

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from hockey_stat.storage.models import TournamentDB


class TournamentDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> t.List[TournamentDB]:
        result = await self.session.execute(sa.select(TournamentDB))
        return list(result.scalars())

    async def get(self, name: str, age: int) -> t.Optional[TournamentDB]:
        result = await self.session.execute(
            sa.select(TournamentDB).where(TournamentDB.name == name, TournamentDB.age == age)
        )
        return result.scalar()

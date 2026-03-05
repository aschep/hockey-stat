import typing as t
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import TeamDB


class TeamDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_team_by_name(self, name: str) -> t.Optional[TeamDB]:
        result = await self.session.execute(
            sa.select(TeamDB)
            .where(TeamDB.name == name)
            .join(TeamDB.players)
            .options(sa.orm.joinedload(TeamDB.players))
        )
        return result.one_or_none()

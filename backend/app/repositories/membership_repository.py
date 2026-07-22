from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.membership import Membership


class MembershipRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

async def create(
    self,
    membership: Membership,
) -> Membership:
    self.db.add(membership)
    await self.db.flush()
    return membership

    async def get_membership(
        self,
        user_id,
        organization_id,
    ):
        result = await self.db.execute(
            select(Membership).where(
                Membership.user_id == user_id,
                Membership.organization_id == organization_id,
            )
        )

        return result.scalar_one_or_none()
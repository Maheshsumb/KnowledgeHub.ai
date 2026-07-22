# app/repositories/organization_repository.py

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.organization import Organization


class OrganizationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        organization: Organization,
    ) -> Organization:
        self.db.add(organization)
        await self.db.flush()
        return organization

    async def get_by_slug(self, slug: str):
        result = await self.db.execute(
            select(Organization).where(
                Organization.slug == slug
            )
        )
        return result.scalar_one_or_none()

    async def get_by_owner(self, owner_id):
        result = await self.db.execute(
            select(Organization).where(
                Organization.owner_id == owner_id
            )
        )
        return result.scalars().all()
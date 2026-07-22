from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.exceptions import OrganizationAlreadyExistsError
from app.models.enums import OrganizationRole
from app.models.membership import Membership
from app.models.organization import Organization
from app.repositories.membership_repository import MembershipRepository
from app.repositories.organization_repository import OrganizationRepository
from app.utils.slug import generate_slug
from app.core.exceptions import (
    OrganizationAlreadyExistsError,
    OrganizationNotFoundError,
)
class OrganizationService:

    def __init__(
        self,
        db: AsyncSession,
        organization_repo: OrganizationRepository,
        membership_repo: MembershipRepository,
    ):
        self.db = db
        self.organization_repo = organization_repo
        self.membership_repo = membership_repo

    async def create(
        self,
        name: str,
        description: str | None,
        owner_id: UUID,
    ) -> Organization:

        slug = generate_slug(name)

        existing = await self.organization_repo.get_by_slug(slug)

        if existing:
            raise OrganizationAlreadyExistsError(
                "Organization already exists."
            )

        organization = Organization(
            name=name,
            slug=slug,
            description=description,
            owner_id=owner_id,
        )

        await self.organization_repo.create(organization)
        membership = Membership(
            user_id=owner_id,
            organization_id=organization.id,
            role=OrganizationRole.OWNER,
        )
        await self.membership_repo.create(membership)
        
        await self.db.commit()
        await self.db.refresh(organization)
        return organization

    async def list(
        self,
        owner_id: UUID,
    ):
        return await self.organization_repo.get_by_owner(
            owner_id
        )

    async def get(
        self,
        organization_id: UUID,
    ):
        organization = await self.organization_repo.get_by_id(
            organization_id
        )

        if organization is None:
            raise OrganizationNotFoundError(
                "Organization not found."
            )

        return organization


    async def update(
        self,
        organization_id: UUID,
        name: str | None,
        description: str | None,
    ):
        organization = await self.get(
            organization_id
        )


        if name is not None:
            organization.name = name
            organization.slug = generate_slug(name)

        if description is not None:
            organization.description = description

        await self.organization_repo.update(
            organization
        )

        await self.db.commit()
        await self.db.refresh(
            organization
        )

        return organization


    async def delete(
        self,
        organization_id: UUID,
    ):
        organization = await self.get(
            organization_id
        )

        await self.organization_repo.delete(
            organization
        )
        await self.db.commit()
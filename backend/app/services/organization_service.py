from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import OrganizationAlreadyExistsError
from app.models.enums import OrganizationRole
from app.models.membership import Membership
from app.models.organization import Organization
from app.repositories.membership_repository import MembershipRepository
from app.repositories.organization_repository import OrganizationRepository
from app.utils.slug import generate_slug


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

        async with self.db.begin():
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
            
        await self.db.refresh(organization)
        return organization

    async def add_member(
        self,
        organization_id,
        user_id,
        role,
    ):
        pass
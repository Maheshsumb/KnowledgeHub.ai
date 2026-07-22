from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    OrganizationNotFoundError,
    UserAlreadyInOrganizationError,
    UserNotFoundError,
    UnauthorizedOrganizationAccessError,
)
from app.models.enums import OrganizationRole
from app.models.membership import Membership
from app.repositories.membership_repository import MembershipRepository
from app.repositories.organization_repository import OrganizationRepository


class MembershipService:

    def __init__(
        self,
        db: AsyncSession,
        membership_repo: MembershipRepository,
        organization_repo: OrganizationRepository,
    ):
        self.db = db
        self.membership_repo = membership_repo
        self.organization_repo = organization_repo

    async def add_member(
        self,
        organization_id: UUID,
        user_id: UUID,
        role: OrganizationRole = OrganizationRole.MEMBER,
    ) -> Membership:

        organization = await self.organization_repo.get_by_id(
            organization_id
        )

        if not organization:
            raise OrganizationNotFoundError(
                "Organization not found."
            )

        existing = await self.membership_repo.get_membership(
            user_id=user_id,
            organization_id=organization_id,
        )

        if existing:
            raise UserAlreadyInOrganizationError(
                "User is already a member of this organization."
            )


        membership = Membership(
            user_id=user_id,
            organization_id=organization_id,
            role=role,
        )

        await self.membership_repo.create(
            membership
        )

        await self.db.commit()
        await self.db.refresh(membership)

        return membership

    async def list_members(
        self,
        organization_id: UUID,
    ):

        organization = await self.organization_repo.get_by_id(
            organization_id
        )

        if not organization:
            raise OrganizationNotFoundError(
                "Organization not found."
            )

        return await self.membership_repo.list_members(
            organization_id
        )

    async def remove_member(
        self,
        organization_id: UUID,
        target_user_id: UUID,
        current_user_id: UUID,
    ):
        current_membership = await self.membership_repo.get_by_user_and_organization(
            current_user_id,
            organization_id,
        )

        target_membership = await self.membership_repo.get_by_user_and_organization(
            target_user_id,
            organization_id,
        )

        if target_membership is None:
            raise UserNotFoundError(
                "Member not found."
            )

        if current_user_id == target_user_id:
            raise UnauthorizedOrganizationAccessError(
                "Use the leave organization endpoint."
            )

        ROLE_HIERARCHY = {
            OrganizationRole.OWNER: 4,
            OrganizationRole.ADMIN: 3,
            OrganizationRole.MEMBER: 2,
            OrganizationRole.VIEWER: 1,
        }

        current_level = ROLE_HIERARCHY[current_membership.role]
        target_level = ROLE_HIERARCHY[target_membership.role]

        if current_level <= target_level:
            raise UnauthorizedOrganizationAccessError(
                "You cannot remove a user with an equal or higher role."
            )

        await self.membership_repo.delete(
            target_membership
        )
        await self.db.commit()

        return None
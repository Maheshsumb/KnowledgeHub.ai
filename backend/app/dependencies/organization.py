from uuid import UUID

from fastapi import Depends, Path

from sqlalchemy.ext.asyncio import AsyncSession

from app.databases.session import get_db
from app.core.auth import get_current_user
from app.models.membership import Membership
from app.models.users import User
from app.repositories.membership_repository import MembershipRepository
from app.core.exceptions import (
    UnauthorizedOrganizationAccessError,
)


async def get_current_membership(
    organization_id: UUID = Path(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Membership:

    repo = MembershipRepository(db)

    membership = await repo.get_user_membership(
        user_id=current_user.id,
        organization_id=organization_id,
    )

    if membership is None:
        raise UnauthorizedOrganizationAccessError(
            "You are not a member of this organization."
        )

    return membership
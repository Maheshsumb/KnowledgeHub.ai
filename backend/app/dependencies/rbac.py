from fastapi import Depends

from app.dependencies.organization import (
    get_current_membership,
)
from app.models.enums import OrganizationRole
from app.models.membership import Membership
from app.core.exceptions import (
    UnauthorizedOrganizationAccessError,
)


ROLE_HIERARCHY = {
    OrganizationRole.OWNER: 4,
    OrganizationRole.ADMIN: 3,
    OrganizationRole.MEMBER: 2,
    OrganizationRole.VIEWER: 1,
}


def require_role(
    minimum_role: OrganizationRole,
):
    async def dependency(
        membership: Membership = Depends(
            get_current_membership
        ),
    ):

        current = ROLE_HIERARCHY[
            membership.role
        ]

        required = ROLE_HIERARCHY[
            minimum_role
        ]

        if current < required:
            raise UnauthorizedOrganizationAccessError(
                "Insufficient permissions."
            )

        return membership

    return dependency
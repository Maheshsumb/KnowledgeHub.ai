import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.membership import Membership
from app.models.enums import OrganizationRole

async def create_membership(
    db: AsyncSession,
    user_id: uuid.UUID,
    organization_id: uuid.UUID,
    role: OrganizationRole = OrganizationRole.MEMBER,
):
    membership = Membership(
        user_id=user_id,
        organization_id=organization_id,
        role=role,
    )
    db.add(membership)
    await db.commit()
    await db.refresh(membership)
    return membership

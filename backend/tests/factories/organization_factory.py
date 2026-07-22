import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.organization import Organization

async def create_organization(
    db: AsyncSession,
    owner_id: uuid.UUID,
    name: str = "Test Organization",
    slug: str = None,
):
    if slug is None:
        slug = f"test-org-{uuid.uuid4().hex[:8]}"
        
    org = Organization(
        name=name,
        slug=slug,
        owner_id=owner_id,
        description="A test organization",
    )
    db.add(org)
    await db.commit()
    await db.refresh(org)
    return org

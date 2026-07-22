from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.databases.session import get_db
from app.core.auth import get_current_user
from app.models.users import User
from app.repositories.organization_repository import OrganizationRepository
from app.repositories.membership_repository import MembershipRepository
from app.schemas.organization import (
    OrganizationCreate,
    OrganizationResponse,
)
from app.services.organization_service import OrganizationService

router = APIRouter(
    prefix="/organizations",
    tags=["Organizations"],
)

@router.post(
    "",
    response_model=OrganizationResponse,
)
async def create_organization(
    request: OrganizationCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    service = OrganizationService(
    db=db,
    organization_repo=OrganizationRepository(db),
    membership_repo=MembershipRepository(db),
)

    return await service.create(
        name=request.name,
        description=request.description,
        owner_id=current_user.id,
    )

@router.get(
    "",
    response_model=list[OrganizationResponse],
)
async def list_organizations(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    service = OrganizationService(
        OrganizationRepository(db)
    )

    return await service.list_user_organizations(
        current_user.id
    )
from uuid import UUID
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.databases.session import get_db
from app.core.auth import get_current_user
from app.dependencies.rbac import require_role
from app.models.enums import OrganizationRole
from app.models.users import User
from app.models.membership import Membership
from app.repositories.organization_repository import OrganizationRepository
from app.repositories.membership_repository import MembershipRepository
from app.schemas.organization import (
    OrganizationCreate,
    OrganizationUpdate,
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
        db=db,
        organization_repo=OrganizationRepository(db),
        membership_repo=MembershipRepository(db),
    )

    return await service.list(
        current_user.id
    )

@router.get(
    "/{organization_id}",
    response_model=OrganizationResponse,
    summary="Get organization details",
)
async def get_organization(
    organization_id: UUID,
    db: AsyncSession = Depends(get_db),
    _: Membership = Depends(
        require_role(OrganizationRole.VIEWER)
    ),
):
    service = OrganizationService(
        db=db,
        organization_repo=OrganizationRepository(db),
        membership_repo=MembershipRepository(db),
    )

    return await service.get(organization_id)

@router.patch(
    "/{organization_id}",
    response_model=OrganizationResponse,
    summary="Update organization",
)
async def update_organization(
    organization_id: UUID,
    request: OrganizationUpdate,
    db: AsyncSession = Depends(get_db),
    _: Membership = Depends(
        require_role(OrganizationRole.ADMIN)
    ),
):
    service = OrganizationService(
        db=db,
        organization_repo=OrganizationRepository(db),
        membership_repo=MembershipRepository(db),
    )

    return await service.update(
        organization_id=organization_id,
        name=request.name,
        description=request.description,
    )

@router.delete(
    "/{organization_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete organization",
)
async def delete_organization(
    organization_id: UUID,
    db: AsyncSession = Depends(get_db),
    _: Membership = Depends(
        require_role(OrganizationRole.OWNER)
    ),
):
    service = OrganizationService(
        db=db,
        organization_repo=OrganizationRepository(db),
        membership_repo=MembershipRepository(db),
    )

    await service.delete(organization_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

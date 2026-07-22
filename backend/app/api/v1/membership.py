from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.databases.session import get_db
from app.dependencies.rbac import require_role
from app.models.enums import OrganizationRole
from app.models.membership import Membership
from app.repositories.membership_repository import MembershipRepository
from app.repositories.organization_repository import OrganizationRepository
from app.schemas.membership import (
    MembershipCreate,
    MembershipUpdate,
    MembershipResponse,
)
from app.services.membership_service import MembershipService

router = APIRouter(
    prefix="/organizations",
    tags=["Memberships"],
)


@router.post(
    "/{organization_id}/members",
    response_model=MembershipResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add a member to an organization",
    description="Allows an Owner or Admin to add a new member to the organization.",
)
async def add_member(
    organization_id: UUID,
    request: MembershipCreate,
    db: AsyncSession = Depends(get_db),
    _: Membership = Depends(
        require_role(OrganizationRole.ADMIN)
    ),
):
    service = MembershipService(
        db=db,
        membership_repo=MembershipRepository(db),
        organization_repo=OrganizationRepository(db),
    )

    return await service.add_member(
        organization_id=organization_id,
        user_id=request.user_id,
        role=request.role,
    )


@router.get(
    "/{organization_id}/members",
    response_model=list[MembershipResponse],
    summary="List organization members",
    description="Returns all members of the organization.",
)
async def list_members(
    organization_id: UUID,
    db: AsyncSession = Depends(get_db),
    _: Membership = Depends(
        require_role(OrganizationRole.VIEWER)
    ),
):
    service = MembershipService(
        db=db,
        membership_repo=MembershipRepository(db),
        organization_repo=OrganizationRepository(db),
    )

    return await service.list_members(
        organization_id=organization_id,
    )


@router.delete(
    "/{organization_id}/members/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove a member",
    description="Allows an Owner or Admin to remove a member from the organization.",
)
async def remove_member(
    organization_id: UUID,
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_membership: Membership = Depends(
        require_role(OrganizationRole.ADMIN)
    ),
):
    service = MembershipService(
        db=db,
        membership_repo=MembershipRepository(db),
        organization_repo=OrganizationRepository(db),
    )

    await service.remove_member(
        organization_id=organization_id,
        target_user_id=user_id,
        current_user_id=current_membership.user_id,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )

@router.patch(
    "/{organization_id}/members/{user_id}",
    response_model=MembershipResponse,
    summary="Update a member's role",
    description="Allows an Owner or Admin to update a member's role.",
)
async def update_member_role(
    organization_id: UUID,
    user_id: UUID,
    request: MembershipUpdate,
    db: AsyncSession = Depends(get_db),
    current_membership: Membership = Depends(
        require_role(OrganizationRole.ADMIN)
    ),
):
    service = MembershipService(
        db=db,
        membership_repo=MembershipRepository(db),
        organization_repo=OrganizationRepository(db),
    )

    return await service.update_role(
        organization_id=organization_id,
        target_user_id=user_id,
        current_user_id=current_membership.user_id,
        new_role=request.role,
    )
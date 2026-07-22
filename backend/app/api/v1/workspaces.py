from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.databases.session import get_db
from app.dependencies.rbac import require_role
from app.models.enums import OrganizationRole
from app.models.membership import Membership
from app.repositories.organization_repository import OrganizationRepository
from app.repositories.workspace_repository import WorkspaceRepository
from app.schemas.workspace import (
    WorkspaceCreate,
    WorkspaceResponse,
    WorkspaceUpdate,
)
from app.services.workspace_service import WorkspaceService

router = APIRouter(
    prefix="/organizations/{organization_id}/workspaces",
    tags=["Workspaces"],
)


def get_workspace_service(
    db: AsyncSession = Depends(get_db),
) -> WorkspaceService:
    return WorkspaceService(
        db=db,
        workspace_repo=WorkspaceRepository(db),
        organization_repo=OrganizationRepository(db),
    )


@router.post(
    "",
    response_model=WorkspaceResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_workspace(
    organization_id: UUID,
    payload: WorkspaceCreate,
    _: Membership = Depends(
        require_role(OrganizationRole.ADMIN)
    ),
    service: WorkspaceService = Depends(
        get_workspace_service
    ),
):
    return await service.create(
        organization_id=organization_id,
        name=payload.name,
        description=payload.description,
    )


@router.get(
    "",
    response_model=list[WorkspaceResponse],
)
async def list_workspaces(
    organization_id: UUID,
    _: Membership = Depends(
        require_role(OrganizationRole.VIEWER)
    ),
    service: WorkspaceService = Depends(
        get_workspace_service
    ),
):
    return await service.list(
        organization_id
    )


@router.get(
    "/{workspace_id}",
    response_model=WorkspaceResponse,
)
async def get_workspace(
    organization_id: UUID,
    workspace_id: UUID,
    _: Membership = Depends(
        require_role(OrganizationRole.VIEWER)
    ),
    service: WorkspaceService = Depends(
        get_workspace_service,
    ),
):
    return await service.get(
        organization_id=organization_id,
        workspace_id=workspace_id,
    )



@router.patch(
    "/{workspace_id}",
    response_model=WorkspaceResponse,
)
async def update_workspace(
    organization_id: UUID,
    workspace_id: UUID,
    payload: WorkspaceUpdate,
    _: Membership = Depends(
        require_role(OrganizationRole.ADMIN)
    ),
    service: WorkspaceService = Depends(
        get_workspace_service,
    ),
):
    return await service.update(
        organization_id=organization_id,
        workspace_id=workspace_id,
        name=payload.name,
        description=payload.description,
    )



@router.delete(
    "/{workspace_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_workspace(
    organization_id: UUID,
    workspace_id: UUID,
    _: Membership = Depends(
        require_role(OrganizationRole.OWNER)
    ),
    service: WorkspaceService = Depends(
        get_workspace_service,
    ),
):
    await service.delete(
        organization_id=organization_id,
        workspace_id=workspace_id,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )
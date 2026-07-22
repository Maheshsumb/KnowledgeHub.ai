from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    File,
    Response,
    UploadFile,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.databases.session import get_db
from app.dependencies.rbac import require_role
from app.models.membership import Membership
from app.models.enums import OrganizationRole
from app.repositories.document_repository import DocumentRepository
from app.repositories.workspace_repository import WorkspaceRepository
from app.schemas.document import DocumentResponse
from app.services.document_service import DocumentService


router = APIRouter(
    prefix="/organizations/{organization_id}/workspaces/{workspace_id}/documents",
    tags=["Documents"],
)


def get_document_service(
    db: AsyncSession = Depends(get_db),
) -> DocumentService:

    return DocumentService(
        db=db,
        document_repo=DocumentRepository(db),
        workspace_repo=WorkspaceRepository(db),
    )


@router.get(
    "",
    response_model=list[DocumentResponse],
)
async def list_documents(
    organization_id: UUID,
    workspace_id: UUID,
    _: Membership = Depends(
        require_role(
            OrganizationRole.VIEWER,
        )
    ),
    service: DocumentService = Depends(
        get_document_service,
    ),
):
    return await service.list_documents(
        organization_id=organization_id,
        workspace_id=workspace_id,
    )


@router.post(
    "",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(
    organization_id: UUID,
    workspace_id: UUID,
    membership: Membership = Depends(
        require_role(
            OrganizationRole.MEMBER,
        )
    ),
    file: UploadFile = File(...),
    service: DocumentService = Depends(
        get_document_service,
    ),
):
    return await service.upload_document(
        organization_id=organization_id,
        workspace_id=workspace_id,
        uploaded_by=membership.user_id,
        file=file,
    )


@router.get(
    "/{document_id}",
    response_model=DocumentResponse,
)
async def get_document(
    organization_id: UUID,
    workspace_id: UUID,
    document_id: UUID,
    _: Membership = Depends(
        require_role(
            OrganizationRole.VIEWER,
        )
    ),
    service: DocumentService = Depends(
        get_document_service,
    ),
):
    return await service.get_document(
        organization_id=organization_id,
        workspace_id=workspace_id,
        document_id=document_id,
    )


@router.delete(
    "/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_document(
    organization_id: UUID,
    workspace_id: UUID,
    document_id: UUID,
    _: Membership = Depends(
        require_role(
            OrganizationRole.ADMIN,
        )
    ),
    service: DocumentService = Depends(
        get_document_service,
    ),
):
    await service.delete_document(
        organization_id=organization_id,
        workspace_id=workspace_id,
        document_id=document_id,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )

from fastapi.responses import FileResponse


@router.get(
    "/{document_id}/download",
)
async def download_document(
    organization_id: UUID,
    workspace_id: UUID,
    document_id: UUID,
    _: Membership = Depends(
        require_role(
            OrganizationRole.VIEWER,
        )
    ),
    service: DocumentService = Depends(
        get_document_service,
    ),
):
    document = await service.get_document(
        organization_id,
        workspace_id,
        document_id,
    )

    return FileResponse(
        path=document.storage_path,
        filename=document.original_filename,
        media_type=document.content_type,
    )
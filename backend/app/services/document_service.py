from uuid import UUID

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    DocumentAlreadyExistsError,
    DocumentNotFoundError,
    WorkspaceNotFoundError,
)

from app.models.document import Document
from app.models.enums import DocumentStatus

from app.repositories.document_repository import (
    DocumentRepository,
)

from app.repositories.workspace_repository import (
    WorkspaceRepository,
)

from app.services.storage_service import StorageService


class DocumentService:

    def __init__(
        self,
        db: AsyncSession,
        document_repo: DocumentRepository,
        workspace_repo: WorkspaceRepository,
    ):
        self.db = db
        self.document_repo = document_repo
        self.workspace_repo = workspace_repo
        self.storage = StorageService()

    async def upload_document(
        self,
        organization_id: UUID,
        workspace_id: UUID,
        uploaded_by: UUID,
        file: UploadFile,
    ) -> Document:

        workspace = await self.workspace_repo.get_by_id(
            organization_id=organization_id,
            workspace_id=workspace_id,
        )

        if workspace is None:
            raise WorkspaceNotFoundError(
                "Workspace not found."
            )

        (
            storage_path,
            file_size,
            checksum,
        ) = await self.storage.save(
            organization_id,
            workspace_id,
            file,
        )

        existing = await self.document_repo.get_by_checksum(
            checksum
        )

        if existing:
            self.storage.delete(storage_path)

            raise DocumentAlreadyExistsError(
                "Document already exists."
            )

        document = Document(
            workspace_id=workspace_id,
            uploaded_by=uploaded_by,

            filename=storage_path.split("/")[-1],
            original_filename=file.filename or "document",

            content_type=file.content_type or "",

            file_size=file_size,

            checksum=checksum,

            storage_path=storage_path,

            status=DocumentStatus.READY,

            metadata_info={},
        )

        async with self.db.begin():

            await self.document_repo.create(
                document
            )

        await self.db.refresh(document)

        return document

    async def list_documents(
        self,
        organization_id: UUID,
        workspace_id: UUID,
    ) -> list[Document]:

        workspace = await self.workspace_repo.get_by_id(
            organization_id=organization_id,
            workspace_id=workspace_id,
        )

        if workspace is None:
            raise WorkspaceNotFoundError(
                "Workspace not found."
            )

        return await self.document_repo.list_by_workspace(
            workspace_id
        )

    async def get_document(
        self,
        organization_id: UUID,
        workspace_id: UUID,
        document_id: UUID,
    ) -> Document:

        workspace = await self.workspace_repo.get_by_id(
            organization_id=organization_id,
            workspace_id=workspace_id,
        )

        if workspace is None:
            raise WorkspaceNotFoundError(
                "Workspace not found."
            )

        document = await self.document_repo.get_by_id(
            workspace_id,
            document_id,
        )

        if document is None:
            raise DocumentNotFoundError(
                "Document not found."
            )

        return document

    async def delete_document(
        self,
        organization_id: UUID,
        workspace_id: UUID,
        document_id: UUID,
    ) -> None:

        document = await self.get_document(
            organization_id,
            workspace_id,
            document_id,
        )

        self.storage.delete(
            document.storage_path
        )

        async with self.db.begin():

            await self.document_repo.delete(
                document
            )
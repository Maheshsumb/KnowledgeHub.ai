from pathlib import Path
from uuid import UUID
import logging

logger = logging.getLogger(__name__)

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.document_chunk_repository import (
    DocumentChunkRepository,
)
from app.services.chunking import ChunkService
from app.core.exceptions import (
    DocumentAlreadyExistsError,
    DocumentNotFoundError,
    WorkspaceNotFoundError,
)
from app.services.embedding.embedding_service import EmbeddingService
from app.services.embedding.providers import QwenEmbeddingProvider
from app.services.vectorstore import ChromaService
from app.models.document import Document
from app.models.enums import DocumentStatus
from app.repositories.document_repository import DocumentRepository
from app.repositories.workspace_repository import WorkspaceRepository
from app.services.ingestion.loader_service import DocumentLoaderService
from app.services.storage_service import StorageService

provider = QwenEmbeddingProvider()
embedding_service = EmbeddingService(provider)
class DocumentService:
    def __init__(
        self,
        db: AsyncSession,
    ) -> None:
        self.db = db

        self.document_repository = DocumentRepository(db)
        self.workspace_repository = WorkspaceRepository(db)
        
        self.storage_service = StorageService()
        self.loader_service = DocumentLoaderService()
        self.chunk_repository = DocumentChunkRepository(db)
        self.chunk_service = ChunkService()
        self.embedding_service = EmbeddingService(
            provider=QwenEmbeddingProvider()
        )

        self.vector_store = ChromaService()
    async def upload_document(
        self,
        organization_id: UUID,
        workspace_id: UUID,
        uploaded_by: UUID,
        file: UploadFile,
    ) -> Document:
        """
        Upload and process a document.
        """

        workspace = await self.workspace_repository.get_by_id(
            organization_id=organization_id,
            workspace_id=workspace_id,
        )

        if workspace is None:
            raise WorkspaceNotFoundError("Workspace not found.")

        (
            storage_path,
            file_size,
            checksum,
        ) = await self.storage_service.save(
            organization_id,
            workspace_id,
            file,
        )

        existing = await self.document_repository.get_by_checksum(
            checksum
        )

        if existing:
            self.storage_service.delete(storage_path)

            raise DocumentAlreadyExistsError(
                "Document already exists."
            )

        document = Document(
            workspace_id=workspace_id,
            uploaded_by=uploaded_by,
            filename=Path(storage_path).name,
            original_filename=file.filename or "document",
            content_type=file.content_type or "",
            file_size=file_size,
            checksum=checksum,
            storage_path=storage_path,
            status=DocumentStatus.UPLOADING,
            metadata_info={},
        )

        document = await self.document_repository.create(
            document
        )

        await self.db.commit()
        await self.db.refresh(document)

        await self._process_document(document)

        return document

    async def list_documents(
        self,
        organization_id: UUID,
        workspace_id: UUID,
    ) -> list[Document]:

        workspace = await self.workspace_repository.get_by_id(
            organization_id=organization_id,
            workspace_id=workspace_id,
        )

        if workspace is None:
            raise WorkspaceNotFoundError(
                "Workspace not found."
            )

        return await self.document_repository.list_by_workspace(
            workspace_id
        )

    async def get_document(
        self,
        organization_id: UUID,
        workspace_id: UUID,
        document_id: UUID,
    ) -> Document:

        workspace = await self.workspace_repository.get_by_id(
            organization_id=organization_id,
            workspace_id=workspace_id,
        )

        if workspace is None:
            raise WorkspaceNotFoundError(
                "Workspace not found."
            )

        document = await self.document_repository.get_by_id(
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

        self.storage_service.delete(
            document.storage_path
        )

        async with self.db.begin():
            await self.document_repository.delete(
                document
            )

    async def _process_document(
        self,
        document: Document,
    ) -> None:
        """
        Process an uploaded document.

        Current pipeline:

            Upload
                ↓
            Parse
                ↓
            READY

        Future pipeline:

            Upload
                ↓
            Parse
                ↓
            Chunk
                ↓
            Embed
                ↓
            Index
                ↓
            READY
        """

        try:
            document.status = DocumentStatus.PROCESSING

            await self.document_repository.update(document)
            await self.db.commit()
            await self.db.refresh(document)
            
            logger.info("Parsing document...")
            parsed_document = await self.loader_service.load(document.storage_path)
            chunks = self.chunk_service.create_chunks(
                document=document,
                parsed_document=parsed_document,
            )
            logger.info("Created %d chunks", len(chunks))

            await self.chunk_repository.delete_by_document(document.id)

            saved_chunks = await self.chunk_repository.create_many(chunks)
            logger.info("Saved %d chunks", len(saved_chunks))

            logger.info("Generating embeddings...")
            embeddings = self.embedding_service.embed_chunks(saved_chunks)
            logger.info("Generated %d embeddings", len(embeddings))

            logger.info("Storing vectors in ChromaDB...")
            self.vector_store.upsert(embeddings)
            logger.info("Stored vectors successfully.")

            document.status = DocumentStatus.READY

            await self.document_repository.update(document)
            await self.db.commit()
            await self.db.refresh(document)

            logger.info("Document processing completed.")

        except Exception:
            document.status = DocumentStatus.FAILED

            await self.document_repository.update(document)
            await self.db.commit()
            await self.db.refresh(document)

            raise
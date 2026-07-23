from __future__ import annotations

import uuid

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document_chunk import DocumentChunk


class DocumentChunkRepository:
    """
    Repository responsible for DocumentChunk database operations.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(
        self,
        chunk: DocumentChunk,
    ) -> DocumentChunk:
        self.db.add(chunk)
        await self.db.flush()
        await self.db.refresh(chunk)
        return chunk

    async def create_many(
        self,
        chunks: list[DocumentChunk],
    ) -> list[DocumentChunk]:
        self.db.add_all(chunks)
        await self.db.flush()

        for chunk in chunks:
            await self.db.refresh(chunk)

        return chunks

    async def get_by_id(
        self,
        chunk_id: uuid.UUID,
    ) -> DocumentChunk | None:
        stmt = (
            select(DocumentChunk)
            .where(DocumentChunk.id == chunk_id)
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def get_by_document(
        self,
        document_id: uuid.UUID,
    ) -> list[DocumentChunk]:
        stmt = (
            select(DocumentChunk)
            .where(DocumentChunk.document_id == document_id)
            .order_by(DocumentChunk.chunk_index)
        )

        result = await self.db.execute(stmt)

        return list(result.scalars().all())

    async def count_by_document(
        self,
        document_id: uuid.UUID,
    ) -> int:
        chunks = await self.get_by_document(document_id)
        return len(chunks)

    async def delete_by_document(
        self,
        document_id: uuid.UUID,
    ) -> None:
        stmt = (
            delete(DocumentChunk)
            .where(DocumentChunk.document_id == document_id)
        )

        await self.db.execute(stmt)
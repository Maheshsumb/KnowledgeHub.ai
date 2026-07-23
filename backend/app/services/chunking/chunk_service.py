from __future__ import annotations

from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.schemas.parsed_document import ParsedDocument

from .splitter import TextSplitter


class ChunkService:
    """
    Converts a ParsedDocument into DocumentChunk objects.
    """

    def __init__(
        self,
        splitter: TextSplitter | None = None,
    ) -> None:
        self.splitter = splitter or TextSplitter()

    def create_chunks(
        self,
        document: Document,
        parsed_document: ParsedDocument,
    ) -> list[DocumentChunk]:
        """
        Create chunk models from parsed text.
        """

        texts = self.splitter.split(
            parsed_document.content
        )

        chunks: list[DocumentChunk] = []

        for index, text in enumerate(texts):

            metadata = {
                **parsed_document.metadata,
                "document_id": str(document.id),
                "workspace_id": str(document.workspace_id),
                "chunk_index": index,
                "source": document.original_filename,
                "content_type": document.content_type,
            }

            chunks.append(
                DocumentChunk(
                    document_id=document.id,
                    chunk_index=index,
                    content=text,
                    metadata_info=metadata,
                    char_count=len(text),
                )
            )

        return chunks
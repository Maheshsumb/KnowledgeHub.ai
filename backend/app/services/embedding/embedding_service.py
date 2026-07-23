from typing import List

from app.models.document_chunk import DocumentChunk
from app.schemas.embedding import ChunkEmbedding
from app.services.embedding.providers.base import BaseEmbeddingProvider
    

class EmbeddingService:
    """
    Generates embeddings for document chunks.
    """

    def __init__(self, provider: BaseEmbeddingProvider):
        self.provider = provider

    @property
    def dimension(self) -> int:
        return self.provider.dimension

    def embed_chunk(
        self,
        chunk: DocumentChunk,
    ) -> ChunkEmbedding:

        embedding = self.provider.embed_text(chunk.content)

        return ChunkEmbedding(
            chunk_id=str(chunk.id),
            content=chunk.content,
            embedding=embedding,
            metadata=chunk.metadata_info,
        )

    def embed_chunks(
        self,
        chunks: List[DocumentChunk],
    ) -> List[ChunkEmbedding]:

        if not chunks:
            return []

        texts = [chunk.content for chunk in chunks]

        vectors = self.provider.embed_texts(texts)

        results = []

        for chunk, vector in zip(chunks, vectors):

            results.append(
                ChunkEmbedding(
                    chunk_id=str(chunk.id),
                    content=chunk.content,
                    embedding=vector,
                    metadata=chunk.metadata_info,
                )
            )

        return results
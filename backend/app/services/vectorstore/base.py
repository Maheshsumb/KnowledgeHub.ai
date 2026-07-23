from abc import ABC, abstractmethod
from typing import List

from app.schemas.embedding import ChunkEmbedding


class BaseVectorStore(ABC):
    """Abstract interface for vector stores."""

    @abstractmethod
    def upsert(self, embeddings: List[ChunkEmbedding]) -> None:
        pass

    @abstractmethod
    def delete_document(self, document_id: str) -> None:
        pass

    @abstractmethod
    def similarity_search(
        self,
        query_embedding: List[float],
        k: int = 5,
    ):
        pass
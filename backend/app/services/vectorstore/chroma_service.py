from typing import List

import chromadb
from chromadb.config import Settings

from app.core.config import settings
from app.schemas.embedding import ChunkEmbedding
from app.services.vectorstore.base import BaseVectorStore


class ChromaService(BaseVectorStore):

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path=settings.CHROMA_DB_PATH,
            settings=Settings(
                anonymized_telemetry=False
            ),
        )

        self.collection = self.client.get_or_create_collection(
            name=settings.CHROMA_COLLECTION,
            metadata={
                "description": "KnowledgeHub AI Vector Store"
            },
        )

    def upsert(
        self,
        embeddings: List[ChunkEmbedding],
    ) -> None:

        if not embeddings:
            return

        self.collection.upsert(
            ids=[
                item.chunk_id
                for item in embeddings
            ],
            documents=[
                item.content
                for item in embeddings
            ],
            embeddings=[
                item.embedding
                for item in embeddings
            ],
            metadatas=[
                item.metadata
                for item in embeddings
            ],
        )

    def delete_document(
        self,
        document_id: str,
    ) -> None:

        self.collection.delete(
            where={
                "document_id": document_id
            }
        )

    def similarity_search(
        self,
        query_embedding: list[float],
        k: int = 5,
        where: dict | None = None,
    ):
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            where=where,
        )
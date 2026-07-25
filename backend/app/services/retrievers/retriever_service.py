from app.schemas.retrieval import (
    RetrievalRequest,
    RetrievalResponse,
    RetrievedChunk,
)
from app.services.embedding.embedding_service import EmbeddingService
from app.services.vectorstore.base import BaseVectorStore


class RetrieverService:
    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: BaseVectorStore,
    ):
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    def retrieve(
        self,
        request: RetrievalRequest,
    ) -> RetrievalResponse:
        
        query_embedding = self.embedding_service.embed_query(
            request.query
        )

        result = self.vector_store.similarity_search(
            query_embedding=query_embedding,
            k=request.top_k,
            where={
                "workspace_id": request.workspace_id
            },
        )

        chunks = []

        ids = result["ids"][0]
        documents = result["documents"][0]
        metadatas = result["metadatas"][0]
        distances = result["distances"][0]

        for chunk_id, document, metadata, distance in zip(
            ids,
            documents,
            metadatas,
            distances,
        ):
            chunks.append(
                RetrievedChunk(
                    chunk_id=chunk_id,
                    document_id=metadata["document_id"],
                    content=document,
                    score=distance,
                    metadata=metadata,
                )
            )

        return RetrievalResponse(
            query=request.query,
            chunks=chunks,
        )
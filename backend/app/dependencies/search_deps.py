from functools import lru_cache

from app.services.embedding.embedding_service import EmbeddingService
from app.services.embedding.providers.qwen_provider import QwenEmbeddingProvider
from app.services.vectorstore.chroma_service import ChromaService
from app.services.retrievers.retriever_service import RetrieverService


@lru_cache
def get_embedding_service():
    provider = QwenEmbeddingProvider()
    return EmbeddingService(provider)


@lru_cache
def get_vector_store():
    return ChromaService()


def get_retriever_service():
    return RetrieverService(
        embedding_service=get_embedding_service(),
        vector_store=get_vector_store(),
    )
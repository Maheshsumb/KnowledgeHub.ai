from functools import lru_cache
from app.services.llm.providers.gemini_provider import GeminiProvider
from app.services.llm.llm_service import LLMService
from app.services.rag.rag_service import RAGService
from app.dependencies.search_deps import get_retriever_service

@lru_cache
def get_llm_service():
    provider = GeminiProvider()

    return LLMService(provider)


@lru_cache
def get_rag_service():

    return RAGService(
        retriever=get_retriever_service(),
        llm=get_llm_service(),
    )

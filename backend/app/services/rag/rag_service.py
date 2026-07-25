from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
    Citation,
)
import time

from app.services.retrievers.retriever_service import RetrieverService
from app.services.rag.context_builder import ContextBuilder
from app.services.rag.prompt_builder import PromptBuilder
from app.services.llm.llm_service import LLMService


class RAGService:

    def __init__(
        self,
        retriever: RetrieverService,
        llm: LLMService,
    ):
        self.retriever = retriever
        self.llm = llm

    def answer(
        self,
        request: ChatRequest,
    ) -> ChatResponse:
        start_time = time.time()

        from app.schemas.retrieval import RetrievalRequest
        retrieval = self.retriever.retrieve(RetrievalRequest(
            query=request.question,
            workspace_id=request.workspace_id,
            top_k=request.top_k,
        ))

        context = ContextBuilder.build(
            retrieval.chunks
        )

        prompt = PromptBuilder.build(
            question=request.question,
            context=context,
        )

        answer = self.llm.generate(
            prompt
        )

        citations = []

        seen = set()

        for chunk in retrieval.chunks:

            document_id = chunk.document_id

            if document_id in seen:
                continue

            seen.add(document_id)

            citations.append(
                Citation(
                    document_id=document_id,
                    source=chunk.metadata.get(
                        "source",
                        "Unknown",
                    ),
                )
            )

        chunks_used = len(retrieval.chunks)
        model_name = self.llm.model_name
        response_time_ms = int((time.time() - start_time) * 1000)

        return ChatResponse(
            answer=answer,
            citations=citations,
            model=model_name,
            chunks_used=chunks_used,
            response_time_ms=response_time_ms,
        )
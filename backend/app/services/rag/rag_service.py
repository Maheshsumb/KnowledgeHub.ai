import time
from typing import Iterator, AsyncIterator
from uuid import UUID

from app.schemas.chat import (
    ChatResponse,
    Citation,
)
from app.core.logging import logger
from app.schemas.retrieval import RetrievalRequest
from app.services.retrievers.retriever_service import RetrieverService
from app.services.rag.context_builder import ContextBuilder
from app.services.rag.prompt_builder import PromptBuilder
from app.services.llm.llm_service import LLMService
from app.services.rag.history_builder import HistoryBuilder


class RAGService:
    """
    Retrieval-Augmented Generation core.

    Responsibilities (only):
      - Retrieve relevant chunks using the rewritten (standalone) question
      - Build a structured context string
      - Build a full LLM prompt (system + history + context + question)
      - Call the LLM and package the response
    """

    def __init__(
        self,
        retriever: RetrieverService,
        llm: LLMService,
        context_builder: ContextBuilder,
        prompt_builder: PromptBuilder,
        history_builder: HistoryBuilder,
    ):
        self.retriever = retriever
        self.llm = llm
        self.context_builder = context_builder
        self.prompt_builder = prompt_builder
        self.history_builder = history_builder

    # ── Internal helpers ──────────────────────────────────────────────────────

    def _retrieve_and_build_prompt(
        self,
        question: str,
        workspace_id: UUID,
        top_k: int,
        history: str,
        rewritten_question: str | None = None,
    ) -> tuple[str, list]:
        """Run retrieval and build the full prompt. Returns (prompt, chunks)."""
        retrieval_query = rewritten_question if rewritten_question else question

        retrieval = self.retriever.retrieve(RetrievalRequest(
            query=retrieval_query,
            workspace_id=workspace_id,
            top_k=top_k,
        ))

        context = self.context_builder.build(chunks=retrieval.chunks)

        prompt = self.prompt_builder.build(
            history=history,
            context=context,
            question=question,
        )

        return prompt, retrieval.chunks

    def _build_citations(self, chunks: list) -> list[Citation]:
        citations: list[Citation] = []
        seen: set = set()

        for chunk in chunks:
            document_id = chunk.document_id
            if document_id in seen:
                continue
            seen.add(document_id)
            citations.append(
                Citation(
                    document_id=document_id,
                    source=chunk.metadata.get("source", "Unknown"),
                )
            )

        return citations

    # ── Public API ────────────────────────────────────────────────────────────

    def answer(
        self,
        question: str,
        workspace_id: UUID,
        top_k: int,
        history: str,
        rewritten_question: str | None = None,
    ) -> ChatResponse:
        start_time = time.time()

        prompt, chunks = self._retrieve_and_build_prompt(
            question=question,
            workspace_id=workspace_id,
            top_k=top_k,
            history=history,
            rewritten_question=rewritten_question,
        )

        answer = self.llm.generate(prompt=prompt)

        return ChatResponse(
            answer=answer,
            citations=self._build_citations(chunks),
            model=self.llm.model_name,
            chunks_used=len(chunks),
            response_time_ms=int((time.time() - start_time) * 1000),
        )

    async def stream_answer(
        self,
        question: str,
        workspace_id: UUID,
        top_k: int,
        history: str,
        rewritten_question: str | None = None,
    ) -> AsyncIterator[str]:
        """
        Retrieve + build prompt, then stream the LLM response token by token.
        Yields raw string tokens only — SSE formatting is handled upstream.
        """
        prompt, _ = self._retrieve_and_build_prompt(
            question=question,
            workspace_id=workspace_id,
            top_k=top_k,
            history=history,
            rewritten_question=rewritten_question,
        )

        async for chunk in self.llm.stream(prompt=prompt):
            yield chunk
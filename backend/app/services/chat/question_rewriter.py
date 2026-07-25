from app.services.llm.llm_service import LLMService
from app.core.logging import logger


class QuestionRewriter:
    """
    Uses the LLM to rewrite a context-dependent follow-up question
    into a fully self-contained standalone question.

    The rewritten question is used ONLY for semantic retrieval.
    The LLM generation step still receives the original question.
    """

    def __init__(
        self,
        llm: LLMService,
    ):
        self.llm = llm

    def rewrite(
        self,
        question: str,
        history: str,
    ) -> str:

        if not history.strip():
            return question

        prompt = f"""Rewrite the user's latest question into a complete, standalone question.

Rules:
- Keep the meaning exactly the same.
- Use conversation history ONLY to resolve references like "it", "that", "this", "he", "she", "they".
- Do NOT answer the question.
- Do NOT add extra context or assumptions beyond what is in the history.
- Return ONLY the rewritten question, nothing else.

Conversation History:

{history}

User's Question:

{question}

Standalone Question:"""

        rewritten = self.llm.generate(prompt=prompt).strip()

        logger.info(
            f"[QuestionRewriter] original='{question}' rewritten='{rewritten}'"
        )

        return rewritten if rewritten else question

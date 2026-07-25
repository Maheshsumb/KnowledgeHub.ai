from app.services.llm.llm_service import LLMService
from app.core.logging import logger


class TitleGenerator:
    """
    Uses the LLM to generate a short, descriptive title for a new conversation
    based on the user's first question.

    The generated title is used to auto-name conversations, replacing the
    generic "New Chat" placeholder.
    """

    def __init__(
        self,
        llm: LLMService,
    ):
        self.llm = llm

    def generate(
        self,
        question: str,
    ) -> str:

        prompt = f"""\
You are an AI that generates short conversation titles.

Rules:
- Maximum 5 words.
- Use Title Case.
- Do not use punctuation.
- Do not include words like: Chat, Conversation, Discussion, Query.
- Return ONLY the title — nothing else.

Question:

{question}

Title:"""

        try:
            title = self.llm.generate(prompt=prompt).strip()
            # Truncate to 100 chars as a safety net for the DB column
            return title[:100] if title else "New Chat"
        except Exception as e:
            logger.warning(f"[TitleGenerator] Failed to generate title: {e}")
            return "New Chat"

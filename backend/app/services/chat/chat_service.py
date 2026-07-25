from typing import Iterator
from uuid import UUID

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.conversation.conversation_service import ConversationService
from app.services.message.message_service import MessageService
from app.services.rag.rag_service import RAGService
from app.services.chat.conversation_formatter import ConversationFormatter
from app.services.chat.question_rewriter import QuestionRewriter
from app.services.chat.title_generator import TitleGenerator
from app.core.logging import logger


class ChatService:
    """
    High-level orchestrator for the end-to-end chat workflow.

    Flow (chat):
      1. Verify conversation ownership
      2. Load recent message window
      3. Format history into plain text
      4. Rewrite follow-up question into a standalone question (for retrieval)
      5. Delegate to RAGService (retrieval + prompting + generation)
      6. Persist user and assistant messages
      7. If first message → generate and save conversation title (background)
      8. Return the response

    Flow (stream_chat):
      Same as above, but streams SSE-formatted tokens.
      Messages and title are updated after the stream completes.
    """

    def __init__(
        self,
        conversation_service: ConversationService,
        message_service: MessageService,
        rag_service: RAGService,
        formatter: ConversationFormatter,
        question_rewriter: QuestionRewriter,
        title_generator: TitleGenerator,
    ):
        self.conversation_service = conversation_service
        self.message_service = message_service
        self.rag_service = rag_service
        self.formatter = formatter
        self.question_rewriter = question_rewriter
        self.title_generator = title_generator

    # ── Shared pre-processing ─────────────────────────────────────────────────

    def _prepare(
        self,
        request: ChatRequest,
        user_id: UUID,
    ) -> tuple[str, str, bool]:
        """Verify ownership, load history, format it, rewrite question.

        Returns (history_text, rewritten_question, is_first_message).
        """
        self.conversation_service.verify_ownership(
            conversation_id=request.conversation_id,
            user_id=user_id,
            workspace_id=request.workspace_id,
        )

        history = self.message_service.list_recent_messages(
            conversation_id=request.conversation_id,
            limit=10,
        )

        is_first_message = len(history) == 0

        history_text = self.formatter.format(history)

        rewritten_question = self.question_rewriter.rewrite(
            question=request.question,
            history=history_text,
        )

        return history_text, rewritten_question, is_first_message

    def _persist(
        self,
        request: ChatRequest,
        answer: str,
    ) -> None:
        """Best-effort message persistence — does not raise on failure."""
        try:
            self.message_service.save_user_message(
                conversation_id=request.conversation_id,
                content=request.question,
            )
            self.message_service.save_assistant_message(
                conversation_id=request.conversation_id,
                content=answer,
            )
        except Exception as e:
            logger.error(
                f"Failed to save messages to conversation "
                f"{request.conversation_id}: {e}"
            )

    def _maybe_set_title(
        self,
        request: ChatRequest,
        is_first_message: bool,
    ) -> None:
        """Generate and save a title if this is the first message in the conversation."""
        if not is_first_message:
            return

        try:
            title = self.title_generator.generate(question=request.question)
            self.conversation_service.update_title(
                conversation_id=request.conversation_id,
                title=title,
            )
            logger.info(
                f"[TitleGenerator] Set title '{title}' "
                f"for conversation {request.conversation_id}"
            )
        except Exception as e:
            logger.warning(
                f"[TitleGenerator] Failed to set title for "
                f"conversation {request.conversation_id}: {e}"
            )

    # ── Public API ────────────────────────────────────────────────────────────

    def chat(
        self,
        request: ChatRequest,
        user_id: UUID,
        background_title: bool = False,
    ) -> tuple[ChatResponse, bool]:
        """
        Returns (response, is_first_message).

        The caller (API layer) should schedule `_maybe_set_title` as a
        BackgroundTask when background_title=True, so the title is generated
        without blocking the HTTP response.
        """
        history_text, rewritten_question, is_first_message = self._prepare(
            request=request,
            user_id=user_id,
        )

        response = self.rag_service.answer(
            question=request.question,
            rewritten_question=rewritten_question,
            workspace_id=request.workspace_id,
            top_k=request.top_k,
            history=history_text,
        )

        self._persist(request=request, answer=response.answer)

        if not background_title:
            self._maybe_set_title(
                request=request,
                is_first_message=is_first_message,
            )

        return response, is_first_message

    def stream_chat(
        self,
        request: ChatRequest,
        user_id: UUID,
    ) -> Iterator[str]:
        """
        Yield SSE-formatted tokens from the LLM, then persist messages and
        optionally auto-title the conversation.

        SSE format:
          data: <token>\\n\\n          — each content token
          event: done\\ndata: complete\\n\\n  — signals end of stream
          event: error\\ndata: <msg>\\n\\n   — on failure
        """
        try:
            history_text, rewritten_question, is_first_message = self._prepare(
                request=request,
                user_id=user_id,
            )

            token_stream = self.rag_service.stream_answer(
                question=request.question,
                rewritten_question=rewritten_question,
                workspace_id=request.workspace_id,
                top_k=request.top_k,
                history=history_text,
            )

            full_answer = ""

            for token in token_stream:
                full_answer += token
                yield f"data: {token}\n\n"

            # Persist messages after stream completes
            self._persist(request=request, answer=full_answer)

            # Auto-title on first message (non-blocking: stream is already done)
            self._maybe_set_title(
                request=request,
                is_first_message=is_first_message,
            )

            yield "event: done\ndata: complete\n\n"

        except Exception as e:
            logger.error(
                f"Streaming error for conversation {request.conversation_id}: {e}"
            )
            yield f"event: error\ndata: {str(e)}\n\n"

from functools import lru_cache

from fastapi import Depends
from sqlalchemy.orm import Session

from app.databases.session import get_db
from app.repositories.conversation_repository import ConversationRepository
from app.repositories.message_repository import MessageRepository
from app.services.chat.chat_service import ChatService
from app.services.chat.conversation_formatter import ConversationFormatter
from app.services.chat.question_rewriter import QuestionRewriter
from app.services.chat.title_generator import TitleGenerator
from app.services.conversation import ConversationService
from app.services.llm.llm_service import LLMService
from app.services.llm.providers.gemini_provider import GeminiProvider
from app.services.message import MessageService
from app.services.rag.context_builder import ContextBuilder
from app.services.rag.history_builder import HistoryBuilder
from app.services.rag.prompt_builder import PromptBuilder
from app.services.rag.rag_service import RAGService
from app.dependencies.search_deps import get_retriever_service


# ── Database repositories ─────────────────────────────────────────────────────

def get_conversation_repository(
    db: Session = Depends(get_db),
) -> ConversationRepository:
    return ConversationRepository(db)


def get_message_repository(
    db: Session = Depends(get_db),
) -> MessageRepository:
    return MessageRepository(db)


# ── Stateless / singleton services ───────────────────────────────────────────

@lru_cache
def get_llm_service() -> LLMService:
    provider = GeminiProvider()
    return LLMService(provider)


@lru_cache
def get_rag_service() -> RAGService:
    return RAGService(
        retriever=get_retriever_service(),
        llm=get_llm_service(),
        context_builder=ContextBuilder(),
        prompt_builder=PromptBuilder(),
        history_builder=HistoryBuilder(),
    )


# ── Request-scoped services ───────────────────────────────────────────────────

def get_conversation_service(
    repository: ConversationRepository = Depends(get_conversation_repository),
) -> ConversationService:
    return ConversationService(repository)


def get_message_service(
    repository: MessageRepository = Depends(get_message_repository),
) -> MessageService:
    return MessageService(repository)


def get_conversation_formatter() -> ConversationFormatter:
    return ConversationFormatter()


def get_question_rewriter() -> QuestionRewriter:
    return QuestionRewriter(llm=get_llm_service())


def get_title_generator() -> TitleGenerator:
    return TitleGenerator(llm=get_llm_service())


def get_chat_service(
    conversation_service: ConversationService = Depends(get_conversation_service),
    message_service: MessageService = Depends(get_message_service),
    rag_service: RAGService = Depends(get_rag_service),
    formatter: ConversationFormatter = Depends(get_conversation_formatter),
    question_rewriter: QuestionRewriter = Depends(get_question_rewriter),
    title_generator: TitleGenerator = Depends(get_title_generator),
) -> ChatService:
    return ChatService(
        conversation_service=conversation_service,
        message_service=message_service,
        rag_service=rag_service,
        formatter=formatter,
        question_rewriter=question_rewriter,
        title_generator=title_generator,
    )
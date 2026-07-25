from fastapi import APIRouter, Depends

from app.dependencies.deps import get_rag_service
from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
)
from app.services.rag.rag_service import RAGService

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "",
    status_code=200,
    response_model=ChatResponse,
)
def chat(
    request: ChatRequest,
    rag_service: RAGService = Depends(
        get_rag_service,
    ),
):
    return rag_service.answer(request)
from fastapi import APIRouter, Depends

from app.schemas.retrieval import (
    RetrievalRequest,
    RetrievalResponse,
)
from app.services.retrievers.retriever_service import RetrieverService
from app.dependencies.search_deps import get_retriever_service

router = APIRouter(
    prefix="/search",
    tags=["Search"]
)


@router.post(
    "",
    status_code=200,
    response_model=RetrievalResponse,
)
def semantic_search(
    request: RetrievalRequest,
    retriever: RetrieverService = Depends(
        get_retriever_service
    ),
):
    return retriever.retrieve(request)
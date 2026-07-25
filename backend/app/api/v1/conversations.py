from uuid import UUID

from fastapi import APIRouter, Depends, Response, status, Query, HTTPException

from app.core.auth import get_current_user
from app.dependencies.deps import (
    get_conversation_service,
)
from app.models.users import User
from app.schemas.conversation import (
    ConversationCreate,
    ConversationRename,
    ConversationResponse,
    ConversationStats,
)
from app.services.conversation import ConversationService

router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"],
)


@router.post(
    "",
    response_model=ConversationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_conversation(
    request: ConversationCreate,
    current_user: User = Depends(get_current_user),
    service: ConversationService = Depends(
        get_conversation_service,
    ),
):
    return service.create_conversation(
        user_id=current_user.id,
        request=request,
    )


@router.get(
    "",
    response_model=list[ConversationResponse],
)
def list_conversations(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    service: ConversationService = Depends(
        get_conversation_service,
    ),
):
    return service.list_conversations(
        user_id=current_user.id,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/search",
    response_model=list[ConversationResponse],
)
def search_conversations(
    query: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    service: ConversationService = Depends(
        get_conversation_service,
    ),
):
    return service.search_conversations(
        user_id=current_user.id,
        query=query,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{conversation_id}",
    response_model=ConversationResponse,
)
def get_conversation(
    conversation_id: UUID,
    service: ConversationService = Depends(
        get_conversation_service,
    ),
):
    return service.get_conversation(
        conversation_id=conversation_id,
    )


@router.patch(
    "/{conversation_id}/title",
    response_model=ConversationResponse,
)
def rename_conversation(
    conversation_id: UUID,
    request: ConversationRename,
    service: ConversationService = Depends(
        get_conversation_service,
    ),
):
    try:
        return service.rename_conversation(
            conversation_id=conversation_id,
            request=request,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post(
    "/{conversation_id}/favorite",
    response_model=ConversationResponse,
)
def favorite_conversation(
    conversation_id: UUID,
    service: ConversationService = Depends(
        get_conversation_service,
    ),
):
    return service.favorite_conversation(
        conversation_id=conversation_id,
    )


@router.post(
    "/{conversation_id}/archive",
    response_model=ConversationResponse,
)
def archive_conversation(
    conversation_id: UUID,
    service: ConversationService = Depends(
        get_conversation_service,
    ),
):
    return service.archive_conversation(
        conversation_id=conversation_id,
    )


@router.post(
    "/{conversation_id}/restore",
    response_model=ConversationResponse,
)
def restore_conversation(
    conversation_id: UUID,
    service: ConversationService = Depends(
        get_conversation_service,
    ),
):
    return service.restore_conversation(
        conversation_id=conversation_id,
    )


@router.get(
    "/{conversation_id}/stats",
    response_model=ConversationStats,
)
def get_conversation_stats(
    conversation_id: UUID,
    service: ConversationService = Depends(
        get_conversation_service,
    ),
):
    return service.get_stats(
        conversation_id=conversation_id,
    )


@router.delete(
    "/{conversation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_conversation(
    conversation_id: UUID,
    service: ConversationService = Depends(
        get_conversation_service,
    ),
):
    service.delete_conversation(
        conversation_id=conversation_id,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )
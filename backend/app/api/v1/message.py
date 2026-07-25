from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

from app.core.auth import get_current_user
from app.dependencies.deps import (
    get_message_service,
)
from app.models.users import User
from app.schemas.message import (
    MessageCreate,
    MessageResponse,
)
from app.services.message import MessageService

router = APIRouter(
    prefix="/messages",
    tags=["Messages"],
)


@router.post(
    "",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_message(
    request: MessageCreate,
    current_user: User = Depends(get_current_user),
    service: MessageService = Depends(
        get_message_service,
    ),
):
    return service.create_message(request)


@router.get(
    "/{conversation_id}",
    response_model=list[MessageResponse],
)
def list_messages(
    conversation_id: UUID,
    current_user: User = Depends(get_current_user),
    service: MessageService = Depends(
        get_message_service,
    ),
):
    return service.list_messages(
        conversation_id,
    )


@router.delete(
    "/{conversation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_messages(
    conversation_id: UUID,
    current_user: User = Depends(get_current_user),
    service: MessageService = Depends(
        get_message_service,
    ),
):
    service.delete_messages(
        conversation_id,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )
from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi.responses import StreamingResponse
from app.core.auth import get_current_user
from app.models.users import User
from app.dependencies.deps import get_chat_service
from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
)
from app.services.chat.chat_service import ChatService

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "",
    status_code=200,
    response_model=ChatResponse,
)
async def chat(
    request: ChatRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    chat_service: ChatService = Depends(
        get_chat_service,
    ),
):
    response, is_first_message = await chat_service.chat(
        request=request,
        user_id=current_user.id,
        background_title=True,
    )

    if is_first_message:
        background_tasks.add_task(
            chat_service._maybe_set_title,
            request=request,
            is_first_message=True,
        )

    return response


@router.post(
    "/stream",
    status_code=200,
    summary="Stream a chat response via Server-Sent Events",
)
async def stream_chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    chat_service: ChatService = Depends(
        get_chat_service,
    ),
):
    return StreamingResponse(
        chat_service.stream_chat(
            request=request,
            user_id=current_user.id,
        ),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )
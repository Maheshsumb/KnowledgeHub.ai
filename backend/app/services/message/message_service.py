from uuid import UUID

from app.models.message import Message
from app.repositories.message_repository import (
    MessageRepository,
)
from app.schemas.message import (
    MessageCreate,
)


class MessageService:

    def __init__(
        self,
        repository: MessageRepository,
    ):
        self.repository = repository

    def create_message(
        self,
        request: MessageCreate,
    ) -> Message:

        message = Message(
            conversation_id=request.conversation_id,
            role=request.role,
            content=request.content,
        )

        return self.repository.create(
            message
        )

    def list_messages(
        self,
        conversation_id: UUID,
    ) -> list[Message]:

        return self.repository.list_by_conversation(
            conversation_id
        )

    def delete_messages(
        self,
        conversation_id: UUID,
    ) -> None:

        self.repository.delete_all(
            conversation_id
        )
    def save_user_message(
    self,
    conversation_id: UUID,
    content: str,
):
        return self.create_message(
            MessageCreate(
            conversation_id=conversation_id,
            role="user",
            content=content,
        )
    )


    def save_assistant_message(
        self,
        conversation_id: UUID,
        content: str,
    ):
        return self.create_message(
            MessageCreate(
            conversation_id=conversation_id,
            role="assistant",
            content=content,
        )
    )

    def get_history(
        self,
        conversation_id: UUID,
        limit: int = 10,
    ) -> list[Message]:

        return self.repository.list_recent_messages(
            conversation_id=conversation_id,
            limit=limit,
        )
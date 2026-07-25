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

    async def create_message(
        self,
        request: MessageCreate,
    ) -> Message:

        message = Message(
            conversation_id=request.conversation_id,
            role=request.role,
            content=request.content,
        )

        return await self.repository.create(
            message
        )

    async def list_messages(
        self,
        conversation_id: UUID,
    ) -> list[Message]:

        return await self.repository.list_by_conversation(
            conversation_id
        )

    async def delete_messages(
        self,
        conversation_id: UUID,
    ) -> None:

        await self.repository.delete_all(
            conversation_id
        )
        
    async def save_user_message(
        self,
        conversation_id: UUID,
        content: str,
    ):
        return await self.create_message(
            MessageCreate(
                conversation_id=conversation_id,
                role="user",
                content=content,
            )
        )

    async def save_assistant_message(
        self,
        conversation_id: UUID,
        content: str,
    ):
        return await self.create_message(
            MessageCreate(
                conversation_id=conversation_id,
                role="assistant",
                content=content,
            )
        )

    async def get_history(
        self,
        conversation_id: UUID,
        limit: int = 10,
    ) -> list[Message]:

        return await self.repository.list_recent_messages(
            conversation_id=conversation_id,
            limit=limit,
        )
from uuid import UUID

from app.models.conversation import Conversation
from app.repositories.conversation_repository import (
    ConversationRepository,
)
from app.schemas.conversation import (
    ConversationCreate,
    ConversationRename,
)


class ConversationService:
    def __init__(
        self,
        repository: ConversationRepository,
    ):
        self.repository = repository

    async def create_conversation(
        self,
        user_id: UUID,
        request: ConversationCreate,
    ) -> Conversation:

        conversation = Conversation(
            title=request.title or "New Chat",
            workspace_id=request.workspace_id,
            user_id=user_id,
        )

        return await self.repository.create(conversation)

    async def get_conversation(
        self,
        conversation_id: UUID,
    ) -> Conversation:

        conversation = await self.repository.get_by_id(
            conversation_id
        )

        if not conversation:
            raise ValueError("Conversation not found")

        return conversation

    async def verify_ownership(
        self,
        conversation_id: UUID,
        user_id: UUID,
        workspace_id: UUID,
    ) -> None:
        conversation = await self.get_conversation(conversation_id)
        if conversation.user_id != user_id:
            raise ValueError("Conversation does not belong to the current user")
        if conversation.workspace_id != workspace_id:
            raise ValueError("Conversation does not belong to the supplied workspace")

    async def update_title(
        self,
        conversation_id: UUID,
        title: str,
    ) -> Conversation:

        conversation = await self.get_conversation(conversation_id)
        conversation.title = title

        return await self.repository.update(conversation)

    async def list_conversations(
        self,
        user_id: UUID,
        workspace_id: UUID | None = None,
        skip: int = 0,
        limit: int = 20,
    ) -> list[Conversation]:
        return await self.repository.list_by_user(
            user_id=user_id,
            workspace_id=workspace_id,
            skip=skip,
            limit=limit,
        )

    async def search_conversations(
        self,
        user_id: UUID,
        query: str,
        workspace_id: UUID | None = None,
        skip: int = 0,
        limit: int = 20,
    ) -> list[Conversation]:
        return await self.repository.search(
            user_id=user_id,
            query=query,
            workspace_id=workspace_id,
            skip=skip,
            limit=limit,
        )

    async def rename_conversation(
        self,
        conversation_id: UUID,
        request: ConversationRename,
    ) -> Conversation:
        conversation = await self.get_conversation(conversation_id)
        
        title = request.title.strip()
        if len(title) < 2 or len(title) > 100:
            raise ValueError("Conversation title must be between 2 and 100 characters")

        conversation.title = title
        return await self.repository.update(conversation)

    async def archive_conversation(
        self,
        conversation_id: UUID,
    ) -> Conversation:
        conversation = await self.get_conversation(conversation_id)
        conversation.is_archived = True
        return await self.repository.update(conversation)

    async def favorite_conversation(
        self,
        conversation_id: UUID,
    ) -> Conversation:
        conversation = await self.get_conversation(conversation_id)
        # Toggle favoriting
        conversation.is_favorite = not conversation.is_favorite
        return await self.repository.update(conversation)

    async def restore_conversation(
        self,
        conversation_id: UUID,
    ) -> Conversation:
        conversation = await self.get_conversation(conversation_id)
        conversation.is_deleted = False
        conversation.is_archived = False
        return await self.repository.update(conversation)

    async def delete_conversation(
        self,
        conversation_id: UUID,
    ) -> None:
        conversation = await self.get_conversation(conversation_id)
        await self.repository.delete(conversation)

    async def get_stats(
        self,
        conversation_id: UUID,
    ) -> dict:
        conversation = await self.get_conversation(conversation_id)
        
        messages_count = conversation.message_count
        
        # We don't save token or document counts on the conversation directly,
        # so we estimate tokens (roughly 4 chars per token) to provide the stat.
        tokens = sum(len(m.content) for m in conversation.messages) // 4
        
        return {
            "messages": messages_count,
            "documents": 0,  # Placeholder unless citation tracking is added
            "tokens": tokens,
            "created_at": conversation.created_at,
        }
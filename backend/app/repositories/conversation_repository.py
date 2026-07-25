from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.conversation import Conversation


class ConversationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        conversation: Conversation,
    ) -> Conversation:
        self.db.add(conversation)
        await self.db.commit()
        await self.db.refresh(conversation)
        return await self.get_by_id(conversation.id)

    async def get_by_id(
        self,
        conversation_id: UUID,
    ) -> Conversation | None:
        stmt = select(Conversation).where(
            Conversation.id == conversation_id
        ).options(selectinload(Conversation.messages))

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_user(
        self,
        user_id: UUID,
        workspace_id: UUID | None = None,
        skip: int = 0,
        limit: int = 20,
    ) -> list[Conversation]:
        conditions = [
            Conversation.user_id == user_id,
            Conversation.is_deleted == False,
        ]
        
        if workspace_id is not None:
            conditions.append(Conversation.workspace_id == workspace_id)
            
        stmt = (
            select(Conversation)
            .where(*conditions)
            .order_by(Conversation.updated_at.desc())
            .offset(skip)
            .limit(limit)
            .options(selectinload(Conversation.messages))
        )

        result = await self.db.scalars(stmt)
        return list(result.all())

    async def search(
        self,
        user_id: UUID,
        query: str,
        workspace_id: UUID | None = None,
        skip: int = 0,
        limit: int = 20,
    ) -> list[Conversation]:
        conditions = [
            Conversation.user_id == user_id,
            Conversation.is_deleted == False,
            Conversation.title.ilike(f"%{query}%")
        ]
        
        if workspace_id is not None:
            conditions.append(Conversation.workspace_id == workspace_id)
            
        stmt = (
            select(Conversation)
            .where(*conditions)
            .order_by(Conversation.updated_at.desc())
            .offset(skip)
            .limit(limit)
            .options(selectinload(Conversation.messages))
        )

        result = await self.db.scalars(stmt)
        return list(result.all())

    async def update(
        self,
        conversation: Conversation,
    ) -> Conversation:
        await self.db.commit()
        await self.db.refresh(conversation)
        return await self.get_by_id(conversation.id)

    async def delete(
        self,
        conversation: Conversation,
    ) -> None:
        conversation.is_deleted = True
        await self.db.commit()
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.message import Message


class MessageRepository:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    async def create(
        self,
        message: Message,
    ) -> Message:

        self.db.add(message)
        await self.db.commit()
        await self.db.refresh(message)

        return message

    async def list_by_conversation(
        self,
        conversation_id: UUID,
    ) -> list[Message]:

        stmt = (
            select(Message)
            .where(
                Message.conversation_id == conversation_id
            )
            .order_by(Message.created_at.asc())
        )

        result = await self.db.scalars(stmt)
        return list(result.all())

    async def delete_all(
        self,
        conversation_id: UUID,
    ) -> None:

        messages = await self.list_by_conversation(
            conversation_id
        )

        for message in messages:
            await self.db.delete(message)

        await self.db.commit()

    async def list_recent_messages(
        self,
        conversation_id: UUID,
        limit: int = 10,
    ) -> list[Message]:
        stmt = (
            select(Message)
            .where(
                Message.conversation_id == conversation_id
            )
            .order_by(Message.created_at.desc())
            .limit(limit)
        )

        result = await self.db.scalars(stmt)
        rows = list(result.all())
        rows.reverse()
        return rows
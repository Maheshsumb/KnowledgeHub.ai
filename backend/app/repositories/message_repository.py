from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.message import Message


class MessageRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def create(
        self,
        message: Message,
    ) -> Message:

        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)

        return message

    def list_by_conversation(
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

        return list(
            self.db.scalars(stmt).all()
        )

    def delete_all(
        self,
        conversation_id: UUID,
    ) -> None:

        messages = self.list_by_conversation(
            conversation_id
        )

        for message in messages:
            self.db.delete(message)

        self.db.commit()

    def list_recent_messages(
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

        rows = list(self.db.scalars(stmt).all())
        rows.reverse()
        return rows
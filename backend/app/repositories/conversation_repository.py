
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.conversation import Conversation


class ConversationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        conversation: Conversation,
    ) -> Conversation:
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)
        return conversation

    def get_by_id(
        self,
        conversation_id: UUID,
    ) -> Conversation | None:
        stmt = select(Conversation).where(
            Conversation.id == conversation_id
        )

        return self.db.scalar(stmt)

    def list_by_user(
        self,
        user_id: UUID,
        skip: int = 0,
        limit: int = 20,
    ) -> list[Conversation]:
        stmt = (
            select(Conversation)
            .where(
                Conversation.user_id == user_id,
                Conversation.is_deleted == False,
            )
            .order_by(Conversation.updated_at.desc())
            .offset(skip)
            .limit(limit)
        )

        return list(self.db.scalars(stmt).all())

    def search(
        self,
        user_id: UUID,
        query: str,
        skip: int = 0,
        limit: int = 20,
    ) -> list[Conversation]:
        stmt = (
            select(Conversation)
            .where(
                Conversation.user_id == user_id,
                Conversation.is_deleted == False,
                Conversation.title.ilike(f"%{query}%")
            )
            .order_by(Conversation.updated_at.desc())
            .offset(skip)
            .limit(limit)
        )

        return list(self.db.scalars(stmt).all())

    def update(
        self,
        conversation: Conversation,
    ) -> Conversation:
        self.db.commit()
        self.db.refresh(conversation)
        return conversation

    def delete(
        self,
        conversation: Conversation,
    ) -> None:
        conversation.is_deleted = True
        self.db.commit()
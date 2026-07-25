from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.databases.base import Base
from app.databases.mixins import TimestampMixin, UUIDMixin


class Message(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "messages"

    conversation_id: Mapped[str] = mapped_column(
        ForeignKey(
            "conversations.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    conversation = relationship(
        "Conversation",
        back_populates="messages",
    )
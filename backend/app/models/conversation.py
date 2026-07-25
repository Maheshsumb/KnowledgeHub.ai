from sqlalchemy import String, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.databases.base import Base
from app.databases.mixins import TimestampMixin, UUIDMixin


class Conversation(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "conversations"

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        default="New Chat",
    )

    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_archived: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_favorite: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    workspace_id: Mapped[str] = mapped_column(
        ForeignKey("workspaces.id", ondelete="CASCADE"),
        nullable=False,
    )

    user = relationship("User")

    workspace = relationship("Workspace")

    messages = relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete-orphan",
        order_by="Message.created_at",
    )

    @property
    def message_count(self) -> int:
        return len(self.messages) if self.messages else 0

    @property
    def last_message(self) -> str | None:
        if self.messages:
            last = self.messages[-1].content
            return last[:100] + "..." if len(last) > 100 else last
        return None
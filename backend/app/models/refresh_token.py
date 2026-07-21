from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.databases.base import Base
from app.databases.mixins import TimestampMixin, UUIDMixin


class RefreshToken(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "refresh_tokens"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    token_id: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    revoked: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    replaced_by: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    user = relationship(
        "User",
        back_populates="refresh_tokens",
    )
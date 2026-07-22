from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column,relationship

from app.databases.base import Base
from app.databases.mixins import TimestampMixin, UUIDMixin


class User(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "users"

    full_name: Mapped[str] = mapped_column(String(255), nullable=False)

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )
    refresh_tokens = relationship(
    "RefreshToken",
    back_populates="user",
    cascade="all, delete-orphan",
    )
    owned_organizations = relationship(
    "Organization",
    back_populates="owner",
    cascade="all, delete-orphan",
    )
    memberships = relationship(
    "Membership",
    back_populates="user",
    cascade="all, delete-orphan",
    )
    uploaded_documents = relationship(
    "Document",
)
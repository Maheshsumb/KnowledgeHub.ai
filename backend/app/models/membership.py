from uuid import UUID

from sqlalchemy import Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.databases.base import Base
from app.databases.mixins import TimestampMixin, UUIDMixin
from app.models.enums import OrganizationRole


class Membership(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "memberships"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "organization_id",
            name="uq_membership_user_org",
        ),
    )

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    organization_id: Mapped[UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
    )

    role: Mapped[OrganizationRole] = mapped_column(
        Enum(
            OrganizationRole,
            name="organization_role",
        ),
        nullable=False,
        default=OrganizationRole.MEMBER,
    )

    user = relationship(
        "User",
        back_populates="memberships",
    )

    organization = relationship(
        "Organization",
        back_populates="memberships",
    )
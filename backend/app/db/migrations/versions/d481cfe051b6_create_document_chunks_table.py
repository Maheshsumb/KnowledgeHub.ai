"""create_document_chunks_table

Revision ID: d481cfe051b6
Revises: d044bf2d58cb
Create Date: 2026-07-24 03:43:46.820824

"""
from typing import Sequence, Union
from sqlalchemy.dialects import postgresql
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd481cfe051b6'
down_revision: Union[str, Sequence[str], None] = 'd044bf2d58cb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "document_chunks",

        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),

        sa.Column(
            "document_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),

        sa.Column(
            "chunk_index",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "content",
            sa.Text(),
            nullable=False,
        ),

        sa.Column(
            "metadata_info",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
        ),

        sa.Column(
            "char_count",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "token_count",
            sa.Integer(),
            nullable=True,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),

        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),

        sa.ForeignKeyConstraint(
            ["document_id"],
            ["documents.id"],
            ondelete="CASCADE",
        ),

        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_document_chunks_document_id",
        "document_chunks",
        ["document_id"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_document_chunks_document_id",
        table_name="document_chunks",
    )

    op.drop_table("document_chunks")
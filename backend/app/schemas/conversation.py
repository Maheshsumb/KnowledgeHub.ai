from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ConversationCreate(BaseModel):
    workspace_id: UUID
    title: str | None = None


class ConversationResponse(BaseModel):
    id: UUID
    title: str
    workspace_id: UUID
    created_at: datetime
    updated_at: datetime
    is_archived: bool
    is_favorite: bool
    message_count: int
    last_message: str | None = None


class ConversationRename(BaseModel):
    title: str = Field(..., min_length=2, max_length=100)


class ConversationStats(BaseModel):
    messages: int
    documents: int
    tokens: int
    created_at: datetime
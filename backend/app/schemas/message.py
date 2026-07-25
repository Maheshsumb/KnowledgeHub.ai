from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class MessageCreate(BaseModel):
    conversation_id: UUID
    role: str
    content: str


class MessageResponse(BaseModel):
    id: UUID
    conversation_id: UUID
    role: str
    content: str
    created_at: datetime
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class DocumentChunkBase(BaseModel):
    chunk_index: int
    content: str
    metadata_info: dict[str, Any]
    char_count: int
    token_count: int | None = None


class DocumentChunkCreate(DocumentChunkBase):
    document_id: uuid.UUID


class DocumentChunkResponse(DocumentChunkBase):
    id: uuid.UUID
    document_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
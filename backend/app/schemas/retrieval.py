from pydantic import BaseModel, Field
from typing import Any


class RetrievalRequest(BaseModel):
    query: str = Field(..., min_length=1)
    workspace_id: str
    top_k: int = Field(default=5, ge=1, le=20)


class RetrievedChunk(BaseModel):
    chunk_id: str
    document_id: str
    content: str
    score: float
    metadata: dict[str, Any]


class RetrievalResponse(BaseModel):

    query: str

    confidence: float

    chunks: list[RetrievedChunk]
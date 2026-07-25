from pydantic import BaseModel
from typing import Any
from typing import Optional
from uuid import UUID



class ChatRequest(BaseModel):
    workspace_id: UUID
    conversation_id: UUID
    question: str
    top_k: int = 5





class Citation(BaseModel):
    document_id: str
    source: str

    page: Optional[int] = None
    chunk_index: Optional[int] = None


class ChatResponse(BaseModel):

    answer: str

    confidence: float

    citations: list[Citation]

    model: str

    chunks_used: int

    response_time_ms: int
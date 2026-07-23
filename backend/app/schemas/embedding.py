from pydantic import BaseModel


class ChunkEmbedding(BaseModel):
    chunk_id: str
    content: str
    embedding: list[float]
    metadata: dict
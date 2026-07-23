from typing import List

from sentence_transformers import SentenceTransformer

from app.core.config import settings
from app.services.embedding.providers.base import BaseEmbeddingProvider


class QwenEmbeddingProvider(BaseEmbeddingProvider):
    """
    Qwen3 embedding provider using SentenceTransformers.
    """

    def __init__(self):
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL)

    def embed_text(self, text: str) -> List[float]:
        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
            convert_to_numpy=True,
        )

        return embedding.tolist()

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            convert_to_numpy=True,
        )

        return embeddings.tolist()

    @property
    def dimension(self) -> int:
        return self.model.get_sentence_embedding_dimension()
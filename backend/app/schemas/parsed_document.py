from typing import Any

from pydantic import BaseModel, Field


class ParsedDocument(BaseModel):
    """
    Normalized document returned by every loader.
    """

    content: str

    title: str | None = None

    page_count: int |None = None

    metadata: dict[str, Any] = Field(default_factory=dict)
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class WorkspaceCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=255,
    )
    description: str | None = Field(
        default=None,
        max_length=1000,
    )


class WorkspaceUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=255,
    )
    description: str | None = Field(
        default=None,
        max_length=1000,
    )


class WorkspaceResponse(BaseModel):
    id: UUID
    organization_id: UUID
    name: str
    slug: str
    description: str | None
    settings: dict
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
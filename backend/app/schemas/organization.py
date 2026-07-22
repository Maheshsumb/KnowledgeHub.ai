from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

class OrganizationUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=255,
    )

    description: str | None = Field(
        default=None,
        max_length=1000,
    )

class OrganizationCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=255,
    )

    description: str | None = Field(
        default=None,
        max_length=1000,
    )

class OrganizationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    slug: str
    description: str | None
    owner_id: UUID
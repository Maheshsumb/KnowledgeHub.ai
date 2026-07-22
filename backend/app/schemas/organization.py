from uuid import UUID

from pydantic import BaseModel, ConfigDict


class OrganizationCreate(BaseModel):
    name: str
    description: str | None = None


class OrganizationUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class OrganizationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    slug: str
    description: str | None
    owner_id: UUID
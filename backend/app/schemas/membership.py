from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.enums import OrganizationRole


class MembershipCreate(BaseModel):
    user_id: UUID
    role: OrganizationRole = OrganizationRole.MEMBER

class MembershipUpdate(BaseModel):
    role: OrganizationRole


class MemberUserResponse(BaseModel):
    id: UUID
    full_name: str
    email: str

class MembershipResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    organization_id: UUID
    role: OrganizationRole
    user: MemberUserResponse | None = None
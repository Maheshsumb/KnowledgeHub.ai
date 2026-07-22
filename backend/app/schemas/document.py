from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.enums import DocumentStatus


class DocumentResponse(BaseModel):
    id: UUID
    workspace_id: UUID
    uploaded_by: UUID | None

    filename: str
    original_filename: str

    content_type: str
    file_size: int

    checksum: str

    storage_path: str

    status: DocumentStatus

    metadata_info: dict

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )
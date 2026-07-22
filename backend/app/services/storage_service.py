import hashlib
import os
import shutil
from pathlib import Path
from uuid import UUID, uuid4

from fastapi import UploadFile


class StorageService:

    STORAGE_ROOT = Path("storage/documents")

    ALLOWED_CONTENT_TYPES = {
        "application/pdf",
        "text/plain",
        "text/markdown",
    }

    MAX_FILE_SIZE = 20 * 1024 * 1024  # 20MB

    def __init__(self):
        self.STORAGE_ROOT.mkdir(
            parents=True,
            exist_ok=True,
        )

    async def save(
        self,
        organization_id: UUID,
        workspace_id: UUID,
        file: UploadFile,
    ) -> tuple[str, int, str]:

        if file.content_type not in self.ALLOWED_CONTENT_TYPES:
            raise ValueError("Unsupported document type.")

        data = await file.read()

        size = len(data)

        if size > self.MAX_FILE_SIZE:
            raise ValueError("File exceeds maximum size.")

        checksum = hashlib.sha256(data).hexdigest()

        extension = Path(
            file.filename or ""
        ).suffix

        filename = f"{uuid4()}{extension}"

        folder = (
            self.STORAGE_ROOT
            / str(organization_id)
            / str(workspace_id)
        )

        folder.mkdir(
            parents=True,
            exist_ok=True,
        )

        path = folder / filename

        with open(path, "wb") as f:
            f.write(data)

        await file.seek(0)

        return (
            str(path),
            size,
            checksum,
        )

    def delete(
        self,
        path: str,
    ) -> None:

        file = Path(path)

        if file.exists():
            file.unlink()
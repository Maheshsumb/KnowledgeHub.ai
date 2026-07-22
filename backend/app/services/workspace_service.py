from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    OrganizationNotFoundError,
    WorkspaceAlreadyExistsError,
    WorkspaceNotFoundError,
)
from app.models.workspace import Workspace
from app.repositories.organization_repository import OrganizationRepository
from app.repositories.workspace_repository import WorkspaceRepository
from app.utils.slug import generate_slug


class WorkspaceService:

    def __init__(
        self,
        db: AsyncSession,
        workspace_repo: WorkspaceRepository,
        organization_repo: OrganizationRepository,
    ):
        self.db = db
        self.workspace_repo = workspace_repo
        self.organization_repo = organization_repo

    async def create(
        self,
        organization_id: UUID,
        name: str,
        description: str | None,
    ) -> Workspace:

        organization = await self.organization_repo.get_by_id(
            organization_id
        )

        if organization is None:
            raise OrganizationNotFoundError(
                "Organization not found."
            )

        slug = generate_slug(name)

        existing = await self.workspace_repo.get_by_slug(
            organization_id=organization_id,
            slug=slug,
        )

        if existing:
            raise WorkspaceAlreadyExistsError(
                "Workspace already exists."
            )

        async with self.db.begin():

            workspace = Workspace(
                organization_id=organization_id,
                name=name,
                slug=slug,
                description=description,
            )

            await self.workspace_repo.create(
                workspace
            )

        await self.db.refresh(workspace)

        return workspace

    async def list(
        self,
        organization_id: UUID,
    ) -> list[Workspace]:

        organization = await self.organization_repo.get_by_id(
            organization_id
        )

        if organization is None:
            raise OrganizationNotFoundError(
                "Organization not found."
            )

        return await self.workspace_repo.list_by_organization(
            organization_id
        )

    async def get(
        self,
        organization_id: UUID,
        workspace_id: UUID,
    ) -> Workspace:

        organization = await self.organization_repo.get_by_id(
            organization_id
        )

        if organization is None:
            raise OrganizationNotFoundError(
                "Organization not found."
            )

        workspace = await self.workspace_repo.get_by_id(
            organization_id=organization_id,
            workspace_id=workspace_id,
        )

        if workspace is None:
            raise WorkspaceNotFoundError(
                "Workspace not found."
            )

        return workspace

    async def update(
        self,
        organization_id: UUID,
        workspace_id: UUID,
        name: str | None,
        description: str | None,
        
    ) -> Workspace:

        workspace = await self.get(
            organization_id=organization_id,
            workspace_id=workspace_id,
        )

        if name is not None:

            slug = generate_slug(name)

            existing = await self.workspace_repo.get_by_slug(
                organization_id=workspace.organization_id,
                slug=slug,
            )

            if (
                existing
                and existing.id != workspace.id
            ):
                raise WorkspaceAlreadyExistsError(
                    "Workspace already exists."
                )

            workspace.name = name
            workspace.slug = slug

        if description is not None:
            workspace.description = description

        await self.workspace_repo.update(
            workspace
        )

        await self.db.commit()
        await self.db.refresh(
            workspace
        )

        return workspace

    async def delete(
        self,
        organization_id: UUID,
        workspace_id: UUID,
    ) -> None:

        workspace = await self.get(
            organization_id=organization_id,
            workspace_id=workspace_id,
        )   

        await self.workspace_repo.delete(
            workspace
        )
        await self.db.commit()
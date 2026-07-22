from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.workspace import Workspace


class WorkspaceRepository:
    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    async def create(
        self,
        workspace: Workspace,
    ) -> Workspace:
        self.db.add(workspace)
        await self.db.flush()
        return workspace

    async def get_by_id(
        self,
        organization_id: UUID,
        workspace_id: UUID,
    ) -> Workspace | None:
        result = await self.db.execute(
            select(Workspace).where(
                Workspace.id == workspace_id,
                Workspace.organization_id == organization_id,
            )
        )

        return result.scalar_one_or_none()

    async def get_by_slug(
        self,
        organization_id: UUID,
        slug: str,
    ) -> Workspace | None:
        result = await self.db.execute(
            select(Workspace).where(
                Workspace.organization_id == organization_id,
                Workspace.slug == slug,
            )
        )

        return result.scalar_one_or_none()

    async def list_by_organization(
        self,
        organization_id: UUID,
    ) -> list[Workspace]:
        result = await self.db.execute(
            select(Workspace).where(
                Workspace.organization_id == organization_id
            )
        )

        return result.scalars().all()

    async def update(
        self,
        workspace: Workspace,
    ) -> Workspace:
        await self.db.flush()
        return workspace

    async def delete(
        self,
        workspace: Workspace,
    ) -> None:
        await self.db.delete(workspace)
        await self.db.flush()
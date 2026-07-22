from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

import traceback
from app.databases.session import get_db

router = APIRouter(prefix="/health", tags=["Health"])


from app.core.config import settings

@router.get("")
def health():
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION
    }

@router.get("/db")
async def db_health(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(text("SELECT current_database(), version();"))
        db_name, version = result.first()

        return {
            "status": "healthy",
            "database": db_name,
            "postgres": version.split(",")[0],
        }


    except Exception as e:
        traceback.print_exc()
        return {
            "status": "unhealthy",
            "error": str(e),
            "type": type(e).__name__,
    }
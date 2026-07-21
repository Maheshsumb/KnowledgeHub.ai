from fastapi import FastAPI
from app.core.logging import logger
from app.api.v1.health import router as health_router
from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.core.exception_handlers import register_exception_handlers
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(users_router)
register_exception_handlers(app)
@app.get("/")
def root():
    return {
        "message": "KnowledgeHub AI Backend"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


from app.core.config import settings

print(settings.DATABASE_URL)
logger.info("KnowledgeHub AI Started")
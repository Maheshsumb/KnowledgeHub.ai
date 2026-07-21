from fastapi import FastAPI
from app.core.logging import logger


from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)


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

logger.info("KnowledgeHub AI Started")
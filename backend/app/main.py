from fastapi import FastAPI
from app.core.logging import logger
from app.api.v1.health import router as health_router
from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.organizations import router as organization_router
from app.core.exception_handlers import register_exception_handlers
from app.core.config import settings
from app.api.v1.membership import router as membership_router
from app.api.v1.workspaces import router as workspaces_router
from app.api.v1.documents import router as documents_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # Allow your Vite frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(health_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(organization_router, prefix="/api/v1")
app.include_router(membership_router, prefix="/api/v1")
app.include_router(workspaces_router, prefix="/api/v1")
app.include_router(documents_router, prefix="/api/v1")
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
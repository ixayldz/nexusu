from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.settings import get_settings
from app.core.logging import setup_logging

# Ayarları yükle → log sistemini ayarla
settings = get_settings()
setup_logging(settings.log_level)

app = FastAPI(title=settings.app_name)

from app.routers import tasks as tasks_router
app.include_router(tasks_router.router)

from app.routers import jobs as jobs_router
app.include_router(jobs_router.router)


# CORS — MVP'de tüm kaynaklara izinli
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["meta"])
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/version", tags=["meta"])
async def version() -> dict[str, str]:
    return {
        "app": settings.app_name,
        "environment": settings.environment,
    }

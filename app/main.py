from __future__ import annotations

# ───────────────────────────────────────────────────────────────
# Temel importlar
# ───────────────────────────────────────────────────────────────
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.core.settings import get_settings
from app.core.logging import setup_logging
from app.core.exceptions import InvalidPlanFormatError

# ───────────────────────────────────────────────────────────────
# Ayarlar & loglama
# ───────────────────────────────────────────────────────────────
settings = get_settings()
setup_logging(settings.log_level)

app = FastAPI(title=settings.app_name)

# ───────────────────────────────────────────────────────────────
# Router'lar
# ───────────────────────────────────────────────────────────────
from app.routers import tasks as tasks_router
from app.routers import jobs as jobs_router

app.include_router(tasks_router.router)
app.include_router(jobs_router.router)

# ───────────────────────────────────────────────────────────────
# Özel exception handler
# ───────────────────────────────────────────────────────────────
@app.exception_handler(InvalidPlanFormatError)
async def invalid_plan_handler(_: Request, exc: InvalidPlanFormatError):
    raise HTTPException(
        status_code=422,
        detail=f"Planner produced invalid JSON: {exc}",
    ) from exc

# ───────────────────────────────────────────────────────────────
# CORS — MVP: tüm kaynaklara izinli
# ───────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ───────────────────────────────────────────────────────────────
# Meta endpoint'ler
# ───────────────────────────────────────────────────────────────
@app.get("/health", tags=["meta"])
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/version", tags=["meta"])
async def version() -> dict[str, str]:
    return {
        "app": settings.app_name,
        "environment": settings.environment,
    }

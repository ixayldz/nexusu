from __future__ import annotations

import asyncio
from pathlib import Path
from typing import List

from pydantic import BaseModel

from app.agents.agent_base import AgentBase
from app.core.model_selector import AgentType, select_model
from app.core.providers import llm_call
from app.core.settings import get_settings

_settings = get_settings()
WS = Path(_settings.workspace_dir)
WS.mkdir(parents=True, exist_ok=True)      # workspace/ oluştur

# ──────────────────────────────────────────────
class BuildRequest(BaseModel):
    steps: List[str]


class BuildFile(BaseModel):
    path: str
    content: str


class BuildResponse(BaseModel):
    success: bool
    files: List[BuildFile]
    written: bool


# ──────────────────────────────────────────────
class BuilderAgent(AgentBase):
    model_name = select_model(AgentType.BUILDER)

    async def run(self, payload: BuildRequest) -> BuildResponse:
        await asyncio.sleep(1)

        # (Gerçek LLM kullanmıyoruz; dosya listesi mock)
        _ = await llm_call(self.model_name)(
            "You generate build scripts", str(payload.steps)
        )

        files = [
            BuildFile(
                path="app/routers/hello.py",
                content="from fastapi import APIRouter\n"
                "router = APIRouter()\n\n"
                "@router.get('/hello')\n"
                "async def hello():\n    return {'msg':'hi'}\n",
            ),
            BuildFile(path="Dockerfile", content="FROM python:3.13-alpine\n"),
        ]

        # Fiziksel olarak yaz
        for f in files:
            abs_path = WS / f.path
            abs_path.parent.mkdir(parents=True, exist_ok=True)
            abs_path.write_text(f.content, encoding="utf-8")

        return BuildResponse(success=True, files=files, written=True)

from __future__ import annotations

import asyncio
import importlib.util
import py_compile
from pathlib import Path
from typing import List

from pydantic import BaseModel

from app.agents.agent_base import AgentBase
from app.core.model_selector import AgentType, select_model
from app.core.providers import llm_call
from app.core.settings import get_settings

_settings = get_settings()
WS = Path(_settings.workspace_dir)

# ──────────────────────────────────────────────
class TestRequest(BaseModel):
    artifacts: List[str]   # dosya yolları (relative)


class TestResponse(BaseModel):
    passed: bool
    score: float
    report: str


# ──────────────────────────────────────────────
class TesterAgent(AgentBase):
    model_name = select_model(AgentType.TESTER)

    async def run(self, payload: TestRequest) -> TestResponse:
        await asyncio.sleep(1)

        # Derleme/ithalat denemesi
        total = len(payload.artifacts)
        ok = 0
        messages = []

        for rel in payload.artifacts:
            p = WS / rel
            try:
                # .py ise derle + import check
                if p.suffix == ".py":
                    py_compile.compile(str(p), doraise=True)
                    spec = importlib.util.spec_from_file_location("tmpmod", p)
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)  # type: ignore
                ok += 1
            except Exception as exc:            # pylint: disable=broad-except
                messages.append(f"{rel}: {exc!s}")

        score = ok / total * 10 if total else 0

        return TestResponse(
            passed=ok == total,
            score=round(score, 2),
            report="\n".join(messages) or "All artifacts compiled/imported OK",
        )

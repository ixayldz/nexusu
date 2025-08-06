from typing import List

from pydantic import BaseModel

from app.agents.agent_base import AgentBase
# ⚡
from app.core.cache import get as cache_get, set as cache_set

from app.core.model_selector import AgentType, select_model  # ekle

class PlannerAgent(AgentBase):
    model_name = select_model(AgentType.PLANNER)             # ekle
    ...



class PlanRequest(BaseModel):
    spec: str


class PlanResponse(BaseModel):
    steps: List[str]


class PlannerAgent(AgentBase):
    async def _generate_plan(self, spec: str) -> PlanResponse:
        """
        Burada gerçek LLM entegrasyonu (Faz 3) gelecek.
        Şimdilik sabit çıktı üretir.
        """
        return PlanResponse(
            steps=[
                "create FastAPI skeleton",
                "add /hello endpoint",
                "write dockerfile",
            ]
        )

    async def run(self, payload: PlanRequest) -> PlanResponse:
        # ⚡ Önce cache’e bak
        cached = await cache_get("plan", payload.model_dump())
        if cached:
            return PlanResponse.model_validate_json(cached)

        # Cache’de yoksa planı üret
        resp = await self._generate_plan(payload.spec)

        # ⚡ Kaydet
        await cache_set(
            "plan",
            payload.model_dump(),
            resp.model_dump_json(),
            ttl=3600,
        )
        return resp

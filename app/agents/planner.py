from __future__ import annotations

import json
from typing import List

from pydantic import BaseModel

from app.agents.agent_base import AgentBase
from app.core.cache import get as cache_get, set as cache_set
from app.core.exceptions import InvalidPlanFormatError
from app.core.model_selector import AgentType, select_model
from app.core.providers import llm_call, LIVE

# --------------------------------------------------------------------- #
# Pydantic modelleri
# --------------------------------------------------------------------- #
class Step(BaseModel):
    id: int
    title: str
    description: str


class PlanRequest(BaseModel):
    spec: str


class PlanResponse(BaseModel):
    steps: List[Step]


# --------------------------------------------------------------------- #
# PlannerAgent
# --------------------------------------------------------------------- #
CACHE_NAMESPACE = "plan_v2"  # v1 (string-liste) verisini bypass ediyoruz


class PlannerAgent(AgentBase):
    model_name = select_model(AgentType.PLANNER)

    # -----------------------------------------------------------
    async def _generate_plan(self, spec: str) -> PlanResponse:
        """
        LLM’den YALNIZCA JSON dizi beklenir:
        [ {"id":1,"title":"...","description":"..."}, ... ]
        LIVE=False iken sabit JSON kullanılır.
        """
        prompt_sys = (
            "You are a senior software architect. "
            "Return ONLY valid JSON array; "
            "each item must have keys id(int), title(str), description(str)."
        )

        if not LIVE:
            steps_json = (
                '[{"id":1,"title":"init","description":"create skeleton"},'
                '{"id":2,"title":"endpoint","description":"add /hello"}]'
            )
        else:
            steps_json = await llm_call(self.model_name)(prompt_sys, spec)

        # JSON metni ➜ Python list ➜ Step doğrulaması
        try:
            raw_list = json.loads(steps_json)
            steps = [Step(**item) for item in raw_list]
        except (json.JSONDecodeError, TypeError, ValueError) as exc:
            raise InvalidPlanFormatError(str(exc)) from exc

        return PlanResponse(steps=steps)

    # -----------------------------------------------------------
    async def run(self, payload: PlanRequest) -> PlanResponse:
        cached = await cache_get(CACHE_NAMESPACE, payload.model_dump())
        if cached:
            return PlanResponse.model_validate_json(cached)

        resp = await self._generate_plan(payload.spec)

        await cache_set(
            CACHE_NAMESPACE, payload.model_dump(), resp.model_dump_json(), ttl=3600
        )
        return resp

from typing import List
import asyncio  # <-- yeni

from pydantic import BaseModel
from app.agents.agent_base import AgentBase

from app.core.model_selector import AgentType, select_model

class BuilderAgent(AgentBase):
    model_name = select_model(AgentType.BUILDER)
    ...



class BuildRequest(BaseModel):
    steps: List[str]


class BuildResponse(BaseModel):
    success: bool
    details: str


class BuilderAgent(AgentBase):
    async def run(self, payload: BuildRequest) -> BuildResponse:
        """
        Mock builder – gerçek kod üretimi Faz 3’te.
        Şimdi 2 sn uyuyup ‘başarılı’ döner.
        """
        await asyncio.sleep(2)  # uzun süren işin yerine geçer
        ok = bool(payload.steps)
        return BuildResponse(
            success=ok,
            details="All steps acknowledged" if ok else "No steps to build",
        )

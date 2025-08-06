from typing import List
import asyncio  # <-- yeni

from pydantic import BaseModel
from app.agents.agent_base import AgentBase

from app.core.model_selector import AgentType, select_model

class TesterAgent(AgentBase):
    model_name = select_model(AgentType.TESTER)
    ...



class TestRequest(BaseModel):
    artifacts: List[str]


class TestResponse(BaseModel):
    passed: bool
    report: str


class TesterAgent(AgentBase):
    async def run(self, payload: TestRequest) -> TestResponse:
        """
        Mock tester – gerçek entegrasyon Faz 3’te.
        2 sn uyuyup ‘passed’ döner.
        """
        await asyncio.sleep(2)
        ok = bool(payload.artifacts)
        return TestResponse(
            passed=ok,
            report="All unit tests passed" if ok else "No artifacts to test",
        )

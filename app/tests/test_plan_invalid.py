import pytest
import app.agents.planner as planner_mod      # modül objesi
from app.agents.planner import PlannerAgent
from app.core.exceptions import InvalidPlanFormatError


def fake_llm_call(_model_name):
    """llm_call(model) yerine geçer – daima bozuk JSON döndürür."""
    async def _bad(_, __):
        return "not-a-list"
    return _bad


@pytest.mark.asyncio
async def test_invalid_plan_format(monkeypatch):
    # 1️⃣ llm_call fabrikasını yamala
    monkeypatch.setattr(planner_mod, "llm_call", fake_llm_call, raising=True)

    # 2️⃣ LIVE=True yap ki stub yolunu atlayıp llm_call yoluna girsin
    monkeypatch.setattr(planner_mod, "LIVE", True, raising=False)

    agent = PlannerAgent()

    with pytest.raises(InvalidPlanFormatError):
        await agent._generate_plan("broken-spec")

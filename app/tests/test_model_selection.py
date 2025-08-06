from app.core.model_selector import AgentType, select_model


def test_model_selector():
    assert select_model(AgentType.PLANNER) == "openai-o3"
    assert select_model(AgentType.BUILDER) == "claude-4-sonnet"
    assert select_model(AgentType.TESTER) == "gemini-2.5-pro"

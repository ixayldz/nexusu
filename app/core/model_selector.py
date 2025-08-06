from enum import Enum

from app.core.settings import get_settings


class AgentType(str, Enum):
    PLANNER = "planner"
    BUILDER = "builder"
    TESTER = "tester"


def select_model(agent: AgentType) -> str:
    """
    Ajan tipine göre Settings.model_map içinden model adını döner.
    Bulunamazsa 'unknown' döner (edge-case).
    """
    mapping = get_settings().model_map
    return mapping.get(agent.value, "unknown")

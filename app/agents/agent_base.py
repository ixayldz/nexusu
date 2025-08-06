from abc import ABC, abstractmethod
from typing import Any

class AgentBase(ABC):
    """
    Tüm ajanların ortak atası – her ajan run() metodunu uygular.
    """

    @abstractmethod
    async def run(self, payload: Any) -> Any:  # pragma: no cover
        raise NotImplementedError
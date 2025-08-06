from abc import ABC, abstractmethod
from typing import Any

class AgentBase(ABC):
    """
    Tüm ajanların ortak atası.
    """

    @abstractmethod
    async def run(self, payload: Any) -> Any:
        """
        Ajanın ana işlevi – alt sınıflar override edecek.
        """
        raise NotImplementedError
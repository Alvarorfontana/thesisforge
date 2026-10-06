from abc import ABC, abstractmethod
from app.models.schemas import ThesisRef

class BaseConnector(ABC):
    name: str = "base"
    origin: str = "global"  # "global" | "argentina"

    @abstractmethod
    async def search(self, query: str, max_results: int = 5) -> list[ThesisRef]: ...

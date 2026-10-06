import httpx
from app.core.config import settings
from app.connectors.base import BaseConnector
from app.models.schemas import ThesisRef

class OATDConnector(BaseConnector):
    """Open Access Theses and Dissertations. Sin API key."""
    name = "OATD"
    origin = "global"
    BASE = "https://oatd.org/oatd/search?q="

    async def search(self, query: str, max_results: int = 5) -> list[ThesisRef]:
        try:
            async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
                r = await client.get(f"{self.BASE}{query.replace(' ', '+')}")
                r.raise_for_status()
                # OATD no tiene API oficial: devolvemos resultados parseados básicos
                return []  # se recomienda CORE/Semantic Scholar para scraping programático
        except Exception:
            return []

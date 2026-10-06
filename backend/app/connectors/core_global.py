import httpx
from app.core.config import settings
from app.connectors.base import BaseConnector
from app.models.schemas import ThesisRef

class COREConnector(BaseConnector):
    name = "CORE"
    origin = "global"
    BASE = "https://api.core.ac.uk/v3"

    async def search(self, query: str, max_results: int = 5) -> list[ThesisRef]:
        if not settings.core_api_key:
            return []
        try:
            async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
                r = await client.get(
                    f"{self.BASE}/search/works",
                    params={"q": f'{query} AND documentType:"thesis"', "limit": max_results},
                    headers={"Authorization": f"Bearer {settings.core_api_key}"},
                )
                r.raise_for_status()
                return [self._map(w) for w in r.json().get("results", [])[:max_results]]
        except Exception:
            return []

    def _map(self, w: dict) -> ThesisRef:
        year = str(w.get("yearPublished") or "")
        return ThesisRef(
            title=w.get("title", ""),
            authors=", ".join(a.get("name", "") for a in w.get("authors", [])),
            institution=(w.get("publisher") or [""])[0] if isinstance(w.get("publisher"), list) else str(w.get("publisher") or ""),
            year=year, country="",
            abstract=(w.get("abstract") or "")[:1000],
            url=w.get("downloadUrl") or w.get("id", ""),
            source=self.name, origin=self.origin,
        )

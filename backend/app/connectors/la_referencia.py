import httpx
from app.core.config import settings
from app.connectors.base import BaseConnector
from app.models.schemas import ThesisRef

class LAReferenciaConnector(BaseConnector):
    """Red federada latinoamericana. Gratis, sin key."""
    name = "LA Referencia"
    origin = "global"  # LatAm
    BASE = "http://www.lareferencia.info/vufind/api/v1"

    async def search(self, query: str, max_results: int = 5) -> list[ThesisRef]:
        try:
            async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
                r = await client.get(f"{self.BASE}/search", params={
                    "lookfor": query, "type": "AllFields", "limit": max_results})
                r.raise_for_status()
                out = []
                for d in r.json().get("resultList", []):
                    out.append(ThesisRef(
                        title=d.get("title", ""),
                        authors=str(d.get("authors", "")),
                        year=str(d.get("year", "") or ""),
                        url=d.get("id", ""),
                        source=self.name, origin=self.origin,
                    ))
                return out
        except Exception:
            return []

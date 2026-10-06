import httpx
from app.core.config import settings
from app.connectors.base import BaseConnector
from app.models.schemas import ThesisRef

class SEDICIConnector(BaseConnector):
    """UNLP. DSpace 7 REST API."""
    name = "SEDICI (UNLP)"
    origin = "argentina"
    BASE = "https://sedici.unlp.edu.ar/server/api"

    async def search(self, query: str, max_results: int = 5) -> list[ThesisRef]:
        try:
            async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
                r = await client.get(f"{self.BASE}/discover/search/objects", params={
                    "query": query, "size": max_results,
                    "configuration": "default"})
                r.raise_for_status()
                out = []
                data = r.json().get("_embedded", {}).get("searchResult", {}).get("_embedded", {}).get("objects", [])
                for obj in data:
                    item = obj.get("_embedded", {}).get("indexableObject", {})
                    title = (item.get("name") or "")
                    out.append(ThesisRef(
                        title=title, institution="UNLP",
                        year=str(item.get("dateIssued", "") or ""),
                        url=item.get("handle", "") or "",
                        source=self.name, origin=self.origin, country="Argentina",
                    ))
                return out[:max_results]
        except Exception:
            return []

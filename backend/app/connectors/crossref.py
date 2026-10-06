import httpx
from app.core.config import settings
from app.connectors.base import BaseConnector
from app.models.schemas import ThesisRef

class CrossrefConnector(BaseConnector):
    """150M+ DOIs. Gratis, sin key (mailto recomendado)."""
    name = "Crossref"
    origin = "global"
    BASE = "https://api.crossref.org/works"

    async def search(self, query: str, max_results: int = 5) -> list[ThesisRef]:
        try:
            async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
                r = await client.get(self.BASE, params={
                    "query": query, "filter": "type:dissertation", "rows": max_results},
                    headers={"User-Agent": "ThesisForge/1.0 (mailto:tu@email.com)"})
                r.raise_for_status()
                out = []
                for it in r.json().get("message", {}).get("items", []):
                    out.append(ThesisRef(
                        title=(it.get("title") or [""])[0],
                        authors=", ".join(" ".join(filter(None, [a.get("given", ""), a.get("family", "")])) for a in it.get("author", [])),
                        institution=(it.get("institution") or [{}])[0].get("name", "") if it.get("institution") else "",
                        year=str((it.get("issued", {}).get("date-parts") or [[None]])[0][0] or ""),
                        url=it.get("URL", ""),
                        source=self.name, origin=self.origin,
                    ))
                return out
        except Exception:
            return []

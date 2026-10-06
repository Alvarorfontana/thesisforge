import httpx
from app.core.config import settings
from app.connectors.base import BaseConnector
from app.models.schemas import ThesisRef

class SemanticScholarConnector(BaseConnector):
    """200M+ papers, gratis, sin API key."""
    name = "Semantic Scholar"
    origin = "global"
    BASE = "https://api.semanticscholar.org/graph/v1"

    async def search(self, query: str, max_results: int = 5) -> list[ThesisRef]:
        try:
            async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
                r = await client.get(
                    f"{self.BASE}/paper/search",
                    params={"query": query, "limit": max_results,
                            "fields": "title,abstract,year,authors,url,venue"},
                )
                r.raise_for_status()
                out = []
                for p in r.json().get("data", []):
                    out.append(ThesisRef(
                        title=p.get("title", ""),
                        authors=", ".join(a.get("name", "") for a in p.get("authors", [])),
                        institution=p.get("venue") or "",
                        year=str(p.get("year") or ""),
                        abstract=(p.get("abstract") or "")[:1000],
                        url=p.get("url", ""),
                        source=self.name, origin=self.origin,
                    ))
                return out
        except Exception:
            return []

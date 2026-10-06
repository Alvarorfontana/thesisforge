import httpx
from app.core.config import settings
from app.connectors.base import BaseConnector
from app.models.schemas import ThesisRef

class OpenAlexConnector(BaseConnector):
    """250M+ obras. Gratis, sin key."""
    name = "OpenAlex"
    origin = "global"
    BASE = "https://api.openalex.org/works"

    async def search(self, query: str, max_results: int = 5) -> list[ThesisRef]:
        try:
            async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
                r = await client.get(
                    self.BASE,
                    params={"search": query, "per-page": max_results,
                            "filter": "type:thesis"},
                )
                r.raise_for_status()
                out = []
                for w in r.json().get("results", []):
                    authorships = w.get("authorships") or []
                    inst = (authorships[0].get("institutions") or [{}])[0].get("display_name", "") if authorships else ""
                    out.append(ThesisRef(
                        title=w.get("display_name", ""),
                        authors=", ".join(a.get("author", {}).get("display_name", "") for a in authorships),
                        institution=inst,
                        year=str(w.get("publication_year") or ""),
                        abstract="", url=w.get("id", ""),
                        source=self.name, origin=self.origin,
                    ))
                return out
        except Exception:
            return []

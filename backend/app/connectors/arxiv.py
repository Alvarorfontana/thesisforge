import httpx
from app.core.config import settings
from app.connectors.base import BaseConnector
from app.models.schemas import ThesisRef

class ArXivConnector(BaseConnector):
    """Preprints en ciencias. Gratis, sin key."""
    name = "arXiv"
    origin = "global"
    BASE = "http://export.arxiv.org/api/query"

    async def search(self, query: str, max_results: int = 5) -> list[ThesisRef]:
        try:
            async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
                r = await client.get(self.BASE, params={
                    "search_query": f"all:{query}", "start": 0, "max_results": max_results})
                r.raise_for_status()
                out = []
                # RSS/Atom simple
                import xml.etree.ElementTree as ET
                ns = {"a": "http://www.w3.org/2005/Atom"}
                tree = ET.fromstring(r.text)
                for e in tree.findall("a:entry", ns):
                    out.append(ThesisRef(
                        title=(e.findtext("a:title", "", ns) or "").strip().replace("\n", " "),
                        authors=", ".join(a.findtext("a:name", "", ns) for a in e.findall("a:author", ns)),
                        institution="arXiv", year="",
                        abstract=(e.findtext("a:summary", "", ns) or "").strip()[:1000],
                        url=(e.findtext("a:id", "", ns) or ""),
                        source=self.name, origin=self.origin,
                    ))
                return out
        except Exception:
            return []

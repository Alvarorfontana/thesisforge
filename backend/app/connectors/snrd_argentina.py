import httpx
from lxml import etree
from app.core.config import settings
from app.connectors.base import BaseConnector
from app.models.schemas import ThesisRef

class SNRDConnector(BaseConnector):
    """Sistema Nacional de Repositorios Digitales (MinCyT). OAI-PMH."""
    name = "SNRD"
    origin = "argentina"
    BASE = "http://snrd.mincyt.gob.ar/oai/request"

    async def search(self, query: str, max_results: int = 5) -> list[ThesisRef]:
        try:
            async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
                r = await client.get(self.BASE, params={
                    "verb": "ListRecords", "metadataPrefix": "oai_dc",
                    "set": "com_123456789_1"})  # ajustar según set
                r.raise_for_status()
                return self._parse(r.text, query, max_results)
        except Exception:
            return []

    def _parse(self, xml_text: str, query: str, max_results: int) -> list[ThesisRef]:
        out = []
        try:
            tree = etree.fromstring(xml_text.encode())
            ns = {"oai": "http://www.openarchives.org/OAI/2.0/",
                  "dc": "http://purl.org/dc/elements/1.1/"}
            for rec in tree.findall(".//oai:record", ns):
                title = (rec.findtext(".//dc:title", "", ns) or "").strip()
                if not title or (query.lower() not in title.lower()):
                    continue
                out.append(ThesisRef(
                    title=title,
                    authors=", ".join(rec.itertext()) if False else (rec.findtext(".//dc:creator", "", ns) or ""),
                    year=rec.findtext(".//dc:date", "", ns) or "",
                    abstract=(rec.findtext(".//dc:description", "", ns) or "")[:1000],
                    url=rec.findtext(".//dc:identifier", "", ns) or "",
                    source=self.name, origin=self.origin, country="Argentina",
                ))
                if len(out) >= max_results:
                    break
        except Exception:
            pass
        return out

import httpx
from app.core.config import settings
from app.connectors.base import BaseConnector
from app.models.schemas import ThesisRef

class UBAAgroConnector(BaseConnector):
    """Repositorio Facultad de Agronomía UBA. OAI-PMH."""
    name = "FAUBA"
    origin = "argentina"
    BASE = "http://repositorio.agro.uba.ar/oai/request"

    async def search(self, query: str, max_results: int = 5) -> list[ThesisRef]:
        try:
            async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
                r = await client.get(self.BASE, params={
                    "verb": "ListRecords", "metadataPrefix": "oai_dc"})
                return self._filter(r.text, query, max_results)
        except Exception:
            return []

    def _filter(self, xml_text: str, query: str, max_results: int) -> list[ThesisRef]:
        out = []
        from lxml import etree
        try:
            tree = etree.fromstring(xml_text.encode())
            ns = {"oai": "http://www.openarchives.org/OAI/2.0/",
                  "dc": "http://purl.org/dc/elements/1.1/"}
            for rec in tree.findall(".//oai:record", ns):
                title = (rec.findtext(".//dc:title", "", ns) or "")
                if query.lower() not in title.lower():
                    continue
                out.append(ThesisRef(
                    title=title.strip(),
                    year=rec.findtext(".//dc:date", "", ns) or "",
                    institution="FAUBA, UBA",
                    url=rec.findtext(".//dc:identifier", "", ns) or "",
                    source=self.name, origin=self.origin, country="Argentina",
                ))
                if len(out) >= max_results:
                    break
        except Exception:
            pass
        return out

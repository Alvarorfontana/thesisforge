import asyncio
from app.core.config import settings
from app.models.schemas import ThesisRef
from app.connectors.semantic_scholar import SemanticScholarConnector
from app.connectors.openalex import OpenAlexConnector
from app.connectors.core_global import COREConnector
from app.connectors.arxiv import ArXivConnector
from app.connectors.la_referencia import LAReferenciaConnector
from app.connectors.crossref import CrossrefConnector
from app.connectors.snrd_argentina import SNRDConnector
from app.connectors.sedici_argentina import SEDICIConnector
from app.connectors.uba_agro import UBAAgroConnector
from app.connectors.conicet import CONICETConnector

CONNECTORS = [
    SemanticScholarConnector(), OpenAlexConnector(), CrossrefConnector(),
    LAReferenciaConnector(), ArXivConnector(), COREConnector(),   # globales
    SNRDConnector(), SEDICIConnector(), UBAAgroConnector(), CONICETConnector(),  # Argentina
]

async def search_all(query: str, max_results: int = None) -> list[ThesisRef]:
    """Consulta todos los repositorios en paralelo y unifica resultados."""
    max_results = max_results or settings.max_results_per_source
    tasks = [asyncio.create_task(c.search(query, max_results)) for c in CONNECTORS]
    # Tope total de 20 s: si un repositorio se cuelga, seguimos con los demás.
    done, pending = await asyncio.wait(tasks, timeout=20)
    for t in pending:
        t.cancel()
    results = []
    for t in done:
        try:
            results.append(t.result())
        except Exception:
            continue

    seen, out = set(), []
    for res in results:
        if isinstance(res, Exception):
            continue
        for ref in res:
            key = ref.title.lower().strip()
            if key and key not in seen:
                seen.add(key)
                out.append(ref)
    # Priorizar resultados argentinos
    out.sort(key=lambda r: 0 if r.origin == "argentina" else 1)
    return out

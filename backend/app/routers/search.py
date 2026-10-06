from fastapi import APIRouter
from app.models.schemas import SearchRequest
from app.services.aggregator import search_all

router = APIRouter()

@router.post("")
async def search(req: SearchRequest):
    results = await search_all(req.query, req.max_results)
    return {"query": req.query, "count": len(results),
            "results": [r.model_dump() for r in results]}

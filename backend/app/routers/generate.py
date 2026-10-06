from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.models.schemas import GenerateRequest
from app.services.aggregator import search_all
from app.services.thesis_engine import build_prompt
from app.services.llm_service import stream_module

router = APIRouter()

@router.post("")
async def generate(req: GenerateRequest):
    references = await search_all(req.topic)
    prompt = build_prompt(req.topic, req.module, req.ideas, references)

    async def event_stream():
        for chunk in stream_module(prompt):
            yield f"data: {chunk}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")

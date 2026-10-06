import json
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.models.schemas import GenerateRequest
from app.services.aggregator import search_all
from app.services.thesis_engine import build_prompt
from app.services.llm_service import stream_module

router = APIRouter()

def _event(kind: str, payload) -> str:
    # Cada evento va en JSON: así los saltos de línea del texto no rompen el SSE.
    return f"data: {json.dumps({'type': kind, 'data': payload}, ensure_ascii=False)}\n\n"

@router.post("")
async def generate(req: GenerateRequest):
    try:
        references = await search_all(req.topic)
    except Exception:
        references = []
    prompt = build_prompt(req.topic, req.module, req.ideas, references)

    # Generador SINCRÓNICO a propósito: Starlette lo corre en un hilo
    # y no bloquea el servidor mientras llega el streaming del LLM.
    def event_stream():
        yield _event("refs", [r.model_dump() for r in references])
        try:
            for chunk in stream_module(prompt):
                yield _event("chunk", chunk)
        except Exception as e:
            yield _event("error", f"Error inesperado del servidor: {e}")
        yield _event("done", "")

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )

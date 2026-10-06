from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import generate, search, projects

app = FastAPI(title="ThesisForge API", version="1.0.0")

# CORS abierto: "*" solo funciona con allow_credentials=False
# (esta app no usa cookies, así que no hace falta).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(generate.router, prefix="/api/generate", tags=["generate"])
app.include_router(search.router, prefix="/api/search", tags=["search"])
app.include_router(projects.router, prefix="/api/projects", tags=["projects"])

@app.get("/")
async def root():
    return {"app": "ThesisForge API", "status": "ok", "health": "/api/health"}

@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "version": "1.0.0",
        "llm_provider": settings.llm_provider,
        "openrouter_key_configured": bool(settings.openrouter_api_key),
    }

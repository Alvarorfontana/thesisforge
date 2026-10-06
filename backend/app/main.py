from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import generate, search, projects

app = FastAPI(title="ThesisForge API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(generate.router, prefix="/api/generate", tags=["generate"])
app.include_router(search.router, prefix="/api/search", tags=["search"])
app.include_router(projects.router, prefix="/api/projects", tags=["projects"])

@app.get("/api/health")
async def health():
    return {"status": "ok", "version": "1.0.0"}

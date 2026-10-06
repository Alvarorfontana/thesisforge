from pydantic import BaseModel
from typing import Optional, List, Literal

ModuleType = Literal["problema", "marco_teorico", "metodologia", "resultados", "discusion", "referencias"]

class GenerateRequest(BaseModel):
    topic: str
    module: ModuleType
    ideas: str = ""
    references: Optional[str] = None

class GenerateResponse(BaseModel):
    module: ModuleType
    content: str
    sources: list = []

class SearchRequest(BaseModel):
    query: str
    max_results: int = 5

class ThesisRef(BaseModel):
    title: str
    authors: str = ""
    institution: str = ""
    country: str = ""
    year: str = ""
    abstract: str = ""
    url: str = ""
    source: str
    origin: str  # "global" | "argentina"

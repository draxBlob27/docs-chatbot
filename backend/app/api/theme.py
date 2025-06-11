from fastapi import APIRouter, Query
from typing import List, Dict
from app.models.schema import ThemeResult
from app.services.search import search
from app.services.citation import attach_citation_to_result
from app.services.summarizer import generate_themes

router = APIRouter()

@router.get("/theme/", response_model=List[ThemeResult])
def theme_endpoint(q: str = Query(...), top_k: int = Query(5)):
    results = search(q, top_k)
    results_with_citations = [attach_citation_to_result(r) for r in results]
    themes = generate_themes(results_with_citations)
    return [theme.model_dump() for theme in themes]


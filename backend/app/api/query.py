from fastapi import APIRouter, Query
from backend.app.services.search import search
from backend.app.services.citation import attach_citation_to_result
from backend.app.models.schema import CitedAnswer
from typing import List

router = APIRouter()

@router.get("/query/", response_model=List[CitedAnswer])
def query_documents(q: str, top_k: int = 5):
    raw_results = search(q, top_k)
    toRet_results = [attach_citation_to_result(res) for res in raw_results]
    return toRet_results

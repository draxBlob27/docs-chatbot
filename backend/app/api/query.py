# For running query from user and return nearest answers found using vector db.

from fastapi import APIRouter
from app.services.search import search
from app.services.citation import attach_citation_to_result
from app.models.schema import CitedAnswer
from typing import List

# Used to be routed by main. 
router = APIRouter()

@router.get("/query/", response_model=List[CitedAnswer])
def query_documents(q: str, top_k: int = 5):    #Recieves query and no of answers to find.
    raw_results = search(q, top_k)  #Searches in vector db for nearest scores.
    toRet_results = [attach_citation_to_result(res) for res in raw_results]   
    return toRet_results    #Returns list of size top_k cited answers

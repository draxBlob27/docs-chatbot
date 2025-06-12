'''
    Response modelling/formatting using pydantic to overcome pythons dynamic nature, 
    used to uniformize and get expected answers.
'''

from typing import Optional, Dict, List #Optinal of x -> union of (x, None)
from pydantic import BaseModel

class UploadResponse(BaseModel):
    filename: str
    chunks_stored: int
    message: str
    error: Optional[str] = None

class SearchResult(BaseModel):
    text: str
    metadata: Dict
    score: float

class CitedAnswer(BaseModel):
    text: str
    citation: str

class ThemeResult(BaseModel):
    theme: str
    summary: str
    citations: List[str]

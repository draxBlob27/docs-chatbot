from typing import Optional, Dict, List
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

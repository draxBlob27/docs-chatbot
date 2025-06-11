from typing import List, Dict
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_file(chunks: List[Dict]) -> List[List[float]]:
    texts = [chunk["text"] for chunk in chunks]
    embeddings = model.encode(texts).tolist()
    return embeddings

def embed_query(query: str) -> List[float]:
    return model.encode(query).tolist()

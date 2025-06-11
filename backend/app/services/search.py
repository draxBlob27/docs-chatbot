
from typing import List, Dict
from sentence_transformers import SentenceTransformer
import chromadb
from backend.app.core.database import collection

model = SentenceTransformer("all-MiniLM-L6-v2")

def search(query: str, top_k: int = 5) -> List[Dict]:
    embedding = model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[embedding], 
        n_results=top_k
    )

    output = []
    for doc, meta, score in zip(results["documents"][0], results["metadatas"][0], results["distances"][0]):
        output.append({
            "text": doc,
            "metadata": meta,
            "score": score
        })
    return output
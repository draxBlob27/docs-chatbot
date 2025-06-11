
from typing import List, Dict
from sentence_transformers import SentenceTransformer
from backend.app.core.database import collection
from backend.app.services.embedding import embed_query

def search(query: str, top_k: int = 5) -> List[Dict]:
    embedding = embed_query(query)
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
'''
    Returns top_k matching list of dictionary of vector embedding, then extracting text, metadata, 
    and relevancy score w.r.t query.
'''


from typing import List, Dict
from app.core.database import collection
from app.services.embedding import embed_query

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
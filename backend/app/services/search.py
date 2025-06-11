
from typing import List, Dict
from sentence_transformers import SentenceTransformer
import chromadb

model = SentenceTransformer("all-MiniLM-L6-v2")

chroma_client = chromadb.PersistentClient(
    path="/Users/sanilparmar/Desktop/wasserStoff_chatbot/backend/data/vectordb"
)
collection = chroma_client.get_or_create_collection(name="document_chunks")


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